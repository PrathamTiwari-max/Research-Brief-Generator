"""
Service for generating research briefs using OpenAI-compatible APIs (like Groq)
"""
import openai
import os
import logging
import json
import re
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class LLMService:
    """Service for generating research briefs using OpenAI/Groq"""
    
    def __init__(self):
        """Initialize LLM service with API key and configuration"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        # Groq/OpenRouter/Other compatibility
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
    
    def _build_prompt(self, articles: List[Dict[str, str]]) -> str:
        """
        Build the specific user prompt requested for multi-source analysis
        """
        source_content = ""
        for i, article in enumerate(articles, 1):
            source_content += f"SOURCE {i}:\n"
            source_content += f"URL: {article['url']}\n"
            source_content += f"CONTENT:\n{article['content']}\n\n"
        
        prompt = f"""{source_content}Return the research brief in EXACTLY this JSON format:

{{
  "summary": "",
  "key_points": [
    {{
      "point": "",
      "source_url": "",
      "source_snippet": ""
    }}
  ],
  "conflicting_claims": [
    {{
      "claim": "",
      "sources": []
    }}
  ],
  "verification_checklist": []
}}

Instructions:
- Compare core claims of each source.
- Identify agreements and shared evidence.
- Identify statements that cannot both be true simultaneously.
- Highlight trade-offs and opposing argumentative viewpoints.
- All source_snippet values must be exact excerpts from the provided content.

Rules:
- Do not include any text outside the JSON.
- Do not wrap in backticks.
- Do not add formatting.
- Populate 'conflicting_claims' when sources make clearly contradictory factual or argumentative statements.
- If one source asserts a claim and another disputes, rejects, or contradicts it, this MUST appear in 'conflicting_claims'.
- If no direct contradiction exists, 'conflicting_claims' must be an empty array [].
- Summary must synthesize across ALL sources."""
        return prompt

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """Defensively extract and parse JSON from LLM response"""
        try:
            # Find first { and last }
            start = text.find('{')
            end = text.rfind('}')
            
            if start == -1 or end == -1:
                raise ValueError("No JSON object found in response")
                
            json_str = text[start:end+1]
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"JSON extraction failed: {str(e)}")
            raise ValueError(f"Failed to parse JSON: {str(e)}")

    def _validate_result(self, result: Any) -> Dict[str, Any]:
        """Validate the LLM response structure and fix common issues"""
        if not isinstance(result, dict):
            raise ValueError("Parsed result is not a JSON object")
        
        required_keys = ["summary", "key_points", "conflicting_claims", "verification_checklist"]
        for key in required_keys:
            if key not in result:
                result[key] = [] if key != "summary" else "No summary generated."
        
        # Ensure correct types
        if not isinstance(result.get("key_points"), list):
            result["key_points"] = []
        if not isinstance(result.get("conflicting_claims"), list):
            result["conflicting_claims"] = []
        if not isinstance(result.get("verification_checklist"), list):
            result["verification_checklist"] = []
            
        return result

    async def generate_brief(self, articles: List[Dict[str, str]]) -> Dict:
        """
        Generate research brief from articles with defensive parsing and retry logic
        """
        user_prompt = self._build_prompt(articles)
        system_prompt = (
            "You are a research analyst.\n"
            "You must synthesize across all provided sources.\n"
            "Compare themes, highlight contrasts, and identify trade-offs.\n"
            "If multiple sources exist, the summary must integrate them into a comparative analysis.\n"
            "Conflicting claims must be generated when one source asserts a claim and another disputes, rejects, or contradicts it.\n"
            "Example: If Source A states 'Human activity causes climate change' and Source B disputes this, it MUST be a conflicting claim.\n"
            "Focus on identifying statements that cannot both be true simultaneously.\n"
            "Do not treat neutral differences as conflict.\n"
            "You must return ONLY valid JSON.\n"
            "No markdown, no emojis, no headings, no explanations.\n"
            "Return raw JSON only."
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        max_retries = 2
        last_raw_response = ""
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Generating research brief (Attempt {attempt + 1}) with model: {self.model}")
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    # Note: Not all providers support json_object mode, so we rely on strict prompting
                    temperature=0.1,
                    max_tokens=3000
                )
                
                last_raw_response = response.choices[0].message.content
                if not last_raw_response:
                    raise ValueError("Empty response from LLM")
                    
                result = self._extract_json(last_raw_response)
                return self._validate_result(result)
                
            except (json.JSONDecodeError, ValueError, Exception) as e:
                logger.warning(f"Generation attempt {attempt + 1} failed: {str(e)}")
                if attempt == 0:
                    messages.append({"role": "assistant", "content": last_raw_response})
                    messages.append({"role": "user", "content": "Return ONLY valid JSON. No explanation."})
                else:
                    # On second failure, raise detailed error for debugging
                    error_msg = f"Failed to parse JSON. Raw response: {last_raw_response[:500]}..."
                    logger.error(error_msg)
                    raise Exception(error_msg)

    def validate_api_key(self) -> bool:
        """Validate LLM configuration with a lightweight request"""
        try:
            self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"LLM configuration validation failed: {str(e)}")
            return False


