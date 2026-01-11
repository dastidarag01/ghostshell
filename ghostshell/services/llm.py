
import json
import re
import time
from typing import Dict, Any, List

from google.genai.types import GenerateContentConfig

from ghostshell.logger import Logger
from ghostshell.prompts import (
    GEMINI_PRO_MODEL, GEMINI_FLASH_MODEL,
    ANALYZE_VOICE_PROMPT, BRAINSTORM_IDEAS_PROMPT, GENERATE_POST_PROMPT,
    PARSE_ADD_MEMORY_PROMPT
)
from ghostshell.models import Blueprint
from ghostshell.constants import LLMProvider


class LLMService:
    def __init__(self, client: Any, provider: LLMProvider):
        self.client = client
        self.provider = provider
        
        # Provider-specific configurations
        if provider == LLMProvider.GEMINI:
            self.deep_model = GEMINI_PRO_MODEL
            self.fast_model = GEMINI_FLASH_MODEL

    def _extract_text_from_response(self, response) -> str:
        if self.provider == LLMProvider.GEMINI:
            text_parts = []
            if response.candidates and len(response.candidates) > 0:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'text') and part.text:
                        text_parts.append(part.text)
            return ''.join(text_parts).strip()
        return str(response)

    def _extract_json_from_text(self, text: str) -> Dict[str, Any]:
        """Extract JSON from LLM response text, handling markdown blocks and extra text."""
        # Strategy 1: Try direct JSON parse first (fastest path)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Strategy 2: Extract from markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Strategy 3: Find first '{' to last '}' and clean
        start_idx = text.find('{')
        end_idx = text.rfind('}')
        if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
            json_str = text[start_idx:end_idx + 1]
            # Remove control characters that break JSON parsing
            json_str = re.sub(r'[\x00-\x1f]', '', json_str)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass

        # All strategies failed
        raise Exception(
            f"Failed to extract valid JSON from LLM response. "
            f"Response preview: {text[:200]}..."
        )

    def _call_llm_json(self, prompt: str, task_desc: str, model: str = None) -> Dict[str, Any]:
        if self.provider == LLMProvider.GEMINI:
            if model is None:
                model = self.fast_model

            max_retries = 3
            for attempt in range(max_retries):
                try:
                    with Logger.status(task_desc):
                        response = self.client.models.generate_content(
                            model=model,
                            contents=prompt,
                            config=GenerateContentConfig(
                                response_mime_type="application/json"
                            )
                        )
                        response_text = self._extract_text_from_response(response)
                        return self._extract_json_from_text(response_text)
                except Exception as e:
                    if attempt < max_retries - 1:
                        # Exponential backoff: 1s, 2s, 4s
                        wait_time = 2 ** attempt
                        Logger.dim(f"Retry {attempt + 1}/{max_retries - 1} after {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise Exception(f"LLM call failed after {max_retries} attempts: {str(e)}")
        
        raise Exception(f"Provider {self.provider} not implemented for JSON generation")

    def parse_add_memory(self, user_input: str) -> Dict[str, Any]:
        prompt = PARSE_ADD_MEMORY_PROMPT.format(user_input=user_input)
        return self._call_llm_json(prompt, "Parsing input...")
    
    def analyze_voice(self, posts_content: str, post_count: int) -> Dict:
        prompt = ANALYZE_VOICE_PROMPT.format(posts_data=posts_content, post_count=post_count)
        provider_name = self.provider.value.title() if isinstance(self.provider, LLMProvider) else str(self.provider).title()
        return self._call_llm_json(prompt, f"Performing deep analysis with {provider_name}...", model=getattr(self, 'deep_model', None))

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

        data = self._call_llm_json(prompt, "Brainstorming ideas...")
        return data['ideas']

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

        provider_name = self.provider.value.title() if isinstance(self.provider, LLMProvider) else str(self.provider).title()
        with Logger.status(f"Generating post with {provider_name}..."):
            if self.provider == LLMProvider.GEMINI:
                response = self.client.models.generate_content(
                    model=self.fast_model,
                    contents=prompt
                )
                return self._extract_text_from_response(response)
        
        raise Exception(f"Provider {self.provider} not implemented for post generation")
