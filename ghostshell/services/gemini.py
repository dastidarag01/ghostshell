
import json
import re
import time
from typing import Dict, Any, List

from google import genai
from google.genai.types import GenerateContentConfig

from ghostshell.logger import Logger
from ghostshell.prompts import (
    GEMINI_PRO_MODEL, GEMINI_FLASH_MODEL,
    ANALYZE_VOICE_PROMPT, BRAINSTORM_IDEAS_PROMPT, GENERATE_POST_PROMPT,
    PARSE_ADD_MEMORY_PROMPT
)
from ghostshell.models import Blueprint


class GeminiClient:

    def __init__(self, api_key: str):
        if not api_key or not api_key.strip():
            raise Exception("API key cannot be empty")

        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        self.pro_model = GEMINI_PRO_MODEL  # For complex voice analysis
        self.flash_model = GEMINI_FLASH_MODEL  # For faster tasks

    def _extract_text_from_response(self, response) -> str:
        text_parts = []
        if response.candidates and len(response.candidates) > 0:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text:
                    text_parts.append(part.text)
        return ''.join(text_parts).strip()

    def _clean_json_string(self, json_str: str) -> str:
        # Remove control characters that break JSON
        json_str = re.sub(r'[\x00-\x1f]', '', json_str)

        # Fix invalid escape sequences - comprehensive approach
        # Match backslash NOT followed by valid JSON escape characters
        # Valid: " \ / b f n r t u (and u must have 4 hex digits)
        json_str = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', json_str)

        # Fix incomplete unicode escapes: \u not followed by 4 hex digits
        json_str = re.sub(r'\\u(?![0-9a-fA-F]{4})', r'\\\\u', json_str)

        return json_str

    def _find_balanced_json(self, text: str) -> str:
        start_idx = text.find('{')
        if start_idx == -1:
            return None

        depth = 0
        in_string = False
        escape = False

        for i in range(start_idx, len(text)):
            char = text[i]

            if escape:
                escape = False
                continue

            if char == '\\':
                escape = True
                continue

            if char == '"':
                in_string = not in_string
                continue

            if not in_string:
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
                    if depth == 0:
                        return text[start_idx:i + 1]

        return None

    def _extract_json_from_response(self, response_text: str) -> str:
        # Strategy 1: Try the whole response as-is
        try:
            json.loads(response_text)
            return response_text
        except json.JSONDecodeError:
            pass

        # Strategy 2: Find balanced braces
        json_str = self._find_balanced_json(response_text)
        if json_str:
            try:
                json.loads(json_str)
                return json_str
            except json.JSONDecodeError:
                pass

        # Strategy 3: Strip markdown code blocks
        stripped = re.sub(r'^```(?:json)?\s*|\s*```$', '', response_text, flags=re.MULTILINE)
        if stripped != response_text:
            try:
                json.loads(stripped)
                return stripped
            except json.JSONDecodeError:
                pass

        # Fallback: return original
        return response_text

    def _generate_json(self, prompt: str, task_desc: str, model: str = None, max_retries: int = 3) -> Dict[str, Any]:
        if model is None:
            model = self.flash_model

        last_error = None

        for attempt in range(max_retries):
            try:
                with Logger.status(task_desc):
                    # Request JSON response type
                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt,
                        config=GenerateContentConfig(
                            response_mime_type="application/json"
                        )
                    )
                    # Phase 1: Use explicit text extraction to avoid SDK warnings
                    response_text = self._extract_text_from_response(response)

                # Phase 4: Try multiple strategies to extract JSON
                json_str = self._extract_json_from_response(response_text)

                # Phase 2: Clean potential invalid escapes
                json_str = self._clean_json_string(json_str)

                # Phase 6: Improved error handling with context
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    if attempt < max_retries - 1:
                        # Transient parsing error - retry
                        wait_time = 2 ** attempt
                        Logger.dim(f"JSON parse error, retrying in {wait_time}s (attempt {attempt + 2}/{max_retries})")
                        time.sleep(wait_time)
                        continue

                    # Final attempt failed - provide detailed error
                    context_start = max(0, e.pos - 30)
                    context_end = min(len(json_str), e.pos + 30)
                    context = json_str[context_start:context_end]
                    raise Exception(
                        f"Failed to parse API response as JSON: {e.msg}\n"
                        f"Error at position {e.pos}\n"
                        f"Context: ...{context}..."
                    )

            except Exception:
                raise
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    Logger.dim(f"API call failed, retrying in {wait_time}s (attempt {attempt + 2}/{max_retries})")
                    time.sleep(wait_time)
                    last_error = e
                    continue
                raise Exception(f"API call failed after {max_retries} attempts: {e}")

    def analyze_voice(self, posts_content: str, post_count: int) -> Dict:
        prompt = ANALYZE_VOICE_PROMPT.format(posts_data=posts_content, post_count=post_count)
        return self._generate_json(prompt, "Performing deep analysis with Gemini Pro...", model=self.pro_model)

    def _validate_brainstorm_response(self, data: Dict) -> List[Dict]:
        if 'ideas' not in data:
            raise Exception("Response missing required 'ideas' key")

        ideas = data['ideas']
        if not isinstance(ideas, list):
            raise Exception(f"'ideas' must be a list, got {type(ideas).__name__}")

        if len(ideas) == 0:
            raise Exception("Response 'ideas' list is empty")

        # Validate each idea has required fields
        for i, idea in enumerate(ideas):
            if not isinstance(idea, dict):
                raise Exception(f"Idea {i+1}: Expected object, got {type(idea).__name__}")

            required = ['topic', 'angle', 'hook_summary']
            missing = [k for k in required if k not in idea]
            if missing:
                raise Exception(f"Idea {i+1} missing required fields: {', '.join(missing)}")

        return ideas

    def brainstorm_ideas(
        self,
        blueprint: Blueprint,
        seed: str = "",
        feedback: list = None,
        ignored_topics: list = None
    ) -> list:
        seed_context = f"INITIAL SEED/FLAVOUR: {seed}" if seed else ""

        feedback_section = ""
        if feedback:
            feedback_list = "\n".join([f"- {f}" for f in feedback])
            feedback_section = f"USER FEEDBACK ON PREVIOUS IDEAS:\n{feedback_list}"

        ignored_section = ""
        if ignored_topics:
            ignored_list = "\n".join([f"{i+1}. {topic}" for i, topic in enumerate(ignored_topics)])
            ignored_section = f"PREVIOUSLY SUGGESTED/IGNORED TOPICS (DO NOT REPEAT):\n{ignored_list}"

        # Add existing topics from blueprint (already posted topics)
        existing_section = ""
        if blueprint.existing_topics:
            existing_list = "\n".join([f"{i+1}. {topic}" for i, topic in enumerate(blueprint.existing_topics)])
            existing_section = f"TOPICS ALREADY POSTED (NEVER SUGGEST THESE):\n{existing_list}"

        prompt = BRAINSTORM_IDEAS_PROMPT.format(
            voice=blueprint.voice,
            core_philosophy=blueprint.core_philosophy,
            target_audience=blueprint.target_audience,
            topic_flavour=blueprint.topic_flavour,
            intellectual_positioning=blueprint.intellectual_positioning,
            anti_patterns=blueprint.anti_patterns,
            seed_context=seed_context,
            feedback_section=feedback_section,
            ignored_section=ignored_section,
            existing_section=existing_section
        )

        data = self._generate_json(prompt, "Brainstorming ideas...")
        # Phase 5: Validate response structure before returning
        return self._validate_brainstorm_response(data)

    def generate_post(self, topic: str, blueprint: Blueprint, feedback: str = None) -> str:
        feedback_section = ""
        if feedback:
            feedback_section = f"\n\nUSER FEEDBACK: {feedback}\nPlease adjust the post based on this feedback."

        prompt = GENERATE_POST_PROMPT.format(
            topic=topic,
            voice=blueprint.voice,
            core_philosophy=blueprint.core_philosophy,
            intellectual_positioning=blueprint.intellectual_positioning,
            topic_flavour=blueprint.topic_flavour,
            target_audience=blueprint.target_audience,
            linguistic_markers=blueprint.linguistic_markers,
            stylistic_fingerprint=blueprint.stylistic_fingerprint,
            hook_pattern=blueprint.opening_hook_psychology,
            narrative_flow=blueprint.narrative_architecture,
            pacing_and_density=blueprint.pacing_and_density,
            anti_patterns=blueprint.anti_patterns,
            feedback_section=feedback_section
        )

        with Logger.status("Generating post with Gemini Flash..."):
            response = self.client.models.generate_content(
                model=self.flash_model,
                contents=prompt
            )
            return self._extract_text_from_response(response)

    def parse_add_memory(self, user_input: str) -> Dict[str, Any]:
        prompt = PARSE_ADD_MEMORY_PROMPT.format(user_input=user_input)
        return self._generate_json(prompt, "Parsing input...")