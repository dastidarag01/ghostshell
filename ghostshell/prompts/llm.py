
# Standardized JSON output instructions for all prompts that require JSON responses
JSON_OUTPUT_INSTRUCTIONS = """
---

# STRICT JSON OUTPUT REQUIREMENTS

**You MUST follow these rules exactly:**

1. **Pure JSON Only**: Return ONLY a valid JSON object. No markdown formatting, no code blocks, no ```json tags, no explanations, no preamble, no postscript.

2. **Character Encoding**:
   - Properly escape all special characters in string values
   - Use double quotes for all strings
   - Escape backslashes as \\\\ (double backslash)
   - Escape quotes as \\"
   - Escape newlines as \\n

3. **String Content Rules**:
   - When including user-provided content, properly escape all quotes and backslashes
   - Do NOT use raw backslashes (\\d, \\s, \\x, etc.) - they must be escaped as \\\\d, \\\\s, \\\\x
   - Use standard JSON escape sequences only: \\", \\\\, \\/, \\b, \\f, \\n, \\r, \\t, \\uXXXX

4. **No Extra Content**:
   - Do NOT include thinking, reasoning, or explanations in the response
   - Do NOT wrap the JSON in any formatting
   - The first character of your response MUST be {{ and the last MUST be }}

5. **Validation**: Before returning, mentally validate that:
   - All braces and brackets are balanced
   - All strings are properly quoted and escaped
   - All arrays and objects are properly formatted
   - The JSON would parse successfully in any standard JSON parser

**Example of CORRECT format:**
The response should start with {{ and end with }}, with properly formatted JSON in between.

**Example of INCORRECT formats to avoid:**
❌ Wrapping in markdown code blocks
❌ Including thinking or explanations before the JSON
❌ Using invalid escape sequences in strings
❌ Adding any text after the closing }}
"""

ANALYZE_VOICE_PROMPT = """You are an expert content strategist and scientific advisor. Your task is to analyze a creator's LinkedIn posts to build a "Voice Blueprint" that captures their unique intellectual DNA.

# YOUR TASK
Forensicly analyze the provided posts to extract the creator's unique intellectual soul.

# DATA PROVIDED
Below are {post_count} LinkedIn posts:

{posts_data}

---

# ANALYSIS DIMENSIONS

## 1. TOPIC FLAVOUR & SCIENTIFIC DOMAINS
Identify the technical "taste" and intellectual interests of the content. 
- What specific scientific or engineering domains are involved? (e.g., Mathematical Physics, Discrete CS, Systems Engineering, Non-parametric Statistics)
- How are these domains blended? (e.g., "Using Physics analogies to explain Software Architecture")
- What level of technical rigor is maintained?

## 2. INTELLECTUAL POSITIONING
How does the creator approach their subjects?
- Is it First-Principles (stripping ideas to the bone)?
- Is it Contrarian (challenging the status quo)?
- Is it Story-First (using narratives to sneak in technical lessons)?
- Is it The Teacher (authoritative but accessible)?

## 3. CORE PHILOSOPHY & TARGET AUDIENCE
- **Philosophy**: What is the "meta-message"? (e.g., "Simplicity over complexity", "Ethics in AI", "The beauty of math")
- **Audience**: Who exactly is this for? (e.g., Senior Engineers, Math hobbyists, VC-backed founders)

## 4. STYLISTIC FINGERPRINT & STRUCTURE
- **Fingerprint**: The rhythm of writing. (e.g., "Short, punchy sentences followed by one deep technical block", "Heavy use of em-dashes and lists")
- **Hook Psychology**: How do they stop the scroll? (e.g., bold claims, curiosity gaps, specific numbers)
- **Narrative Architecture**: How do they move from hook to body to CTA?

---

# OUTPUT FORMAT

Return a valid JSON object with this exact flat structure:

{{
  "voice": "Tone and personality description (2-3 sentences).",
  "core_philosophy": "The primary belief system or meta-message found in the writing.",
  "target_audience": "The specific persona being addressed.",
  "niche": "The broad domain of expertise.",
  
  "intellectual_positioning": "How the creator thinks and positions their arguments.",
  "topic_flavour": "Categorization of intellectual interests and domains (e.g., Math, CS, Physics) and their specific 'taste'.",
  "linguistic_markers": "Nuanced vocabulary, recurring phrases, and signature expressions.",
  
  "stylistic_fingerprint": "Description of sentence rhythm, formatting patterns, and visual density.",
  "opening_hook_psychology": "Detailed analysis of how and why their hooks work.",
  "narrative_architecture": "The common structural flow from opening to call-to-action.",
  "pacing_and_density": "Balance between complex information and readability/whitespace.",
  
  "anti_patterns": "What this creator NEVER does (specific and actionable)."
}}

# CRITICAL RULES
1. **No Generic Content**: Avoid "authoritative tone" or "technical niche". Use "Assertive Mathematical Rigor" and "Distributed Systems Optimization".
2. **Contextual Flavour**: Capture the domains (Math, Physics, CS) as guiding interests, not rigid constraints.
3. **Flat Structure**: Do NOT nest fields. Follow the structure above exactly.
4. **No Unicodes**: Do not include any unicode characters in the output.
""" + JSON_OUTPUT_INSTRUCTIONS

BRAINSTORM_IDEAS_PROMPT = """Based on the creator's Voice Blueprint, suggest 5 specific LinkedIn post ideas.

# INPUT CONTEXT
Voice: {voice}
Core Philosophy: {core_philosophy}
Target Audience: {target_audience}
Topic Flavour: {topic_flavour}
Intellectual Positioning: {intellectual_positioning}
Anti-patterns: {anti_patterns}

{seed_context}
{feedback_section}
{ignored_section}
{existing_section}

# BRAINSTORMING CONSTRAINTS
1. **DOMAIN HARMONY**: Ideas should be "flavoured" by the `{topic_flavour}`, but prioritize the `{intellectual_positioning}` and `{voice}`. Use the favour as a guiding interest, not a rigid boundary.
2. **PHILOSOPHY FIRST**: Every post must subtly reflect the `{core_philosophy}`.
3. **DEDUPLICATION**: NEVER suggest anything semantically similar to topics already posted or ignored.

# OUTPUT FORMAT
Return a JSON object with this exact structure:

{{
  "ideas": [
    {{
      "topic": "Complete descriptive sentence (10-15 words) explaining the technical concept/lesson",
      "angle": "The specific perspective matching the {intellectual_positioning}",
      "hook_summary": "Summary of the hook strategy"
    }}
  ]
}}
""" + JSON_OUTPUT_INSTRUCTIONS

GENERATE_POST_PROMPT = """Write an article for LinkedIn based on this Blueprint.

# TOPIC: {topic}

# VOICE BLUEPRINT
Voice: {voice}

# INSTRUCTIONS
1. **Embody the Positioning**: Write as a `{intellectual_positioning}`.
2. **Infuse the Flavour**: Use the `{topic_flavour}` as a supporting layer for the topic depth.
3. **Address the Audience**: Speak directly to the needs of `{target_audience}`.
4. **Subtle Philosophy**: Weave in the `{core_philosophy}` naturally.
5. **No Preamble**: Return ONLY the post content.
6. **Plain Text Only**: Do not include any unicode characters or markdown formatting in the output.

# STYLE OUTLINE
Markers: {linguistic_markers}
Stylistic Fingerprint: {stylistic_fingerprint}
Hook Psychology: {hook_pattern}
Narrative Architecture: {narrative_flow}
Pacing/Density: {pacing_and_density}
Anti-patterns: {anti_patterns}

{feedback_section}"""

PARSE_ADD_MEMORY_PROMPT = """Parse the following free-text input into a structured memory format.

The user will provide:
- Post content (the LinkedIn post text)

Extract and structure this information.

USER INPUT:
{user_input}

Return a JSON object with this structure:
{{
  "content": "The full LinkedIn post content",
  "topic": "A descriptive sentence (10-15 words) explaining what the post covers (e.g., 'How Quake III used a magic constant to calculate inverse square roots incredibly fast', 'Bloom Filters enable fast membership testing using probabilistic data structures')"
}}

INSTRUCTIONS:
- Extract the main post content as is (usually the longest text block)
- Generate a descriptive topic sentence (10-15 words) that explains what the post is about
- The topic should be specific and actionable (e.g., "How HyperLogLog Algorithm estimates cardinality using minimal memory", not "Data Structures")
""" + JSON_OUTPUT_INSTRUCTIONS
