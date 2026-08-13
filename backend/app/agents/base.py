import json
import re
import httpx
import logging
from typing import Dict, Any, Optional
from app.config import OLLAMA_HOST, OLLAMA_MODEL

logger = logging.getLogger(__name__)

async def call_ollama(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.3,
    json_mode: bool = False
) -> str:
    """
    Asynchronously invokes the local Ollama LLM (gemma4:latest).
    """
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 4096
        }
    }
    if system_prompt:
        payload["system"] = system_prompt
    if json_mode:
        payload["format"] = "json"

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except Exception as e:
            logger.error(f"Error calling Ollama API ({OLLAMA_MODEL}): {e}")
            raise RuntimeError(f"Ollama local LLM call failed: {e}")

def extract_json(text: str) -> Dict[str, Any]:
    """
    Robust JSON extraction engine capable of handling code blocks, extra text,
    and minor formatting errors from local 8B LLMs.
    """
    if not text:
        return {}
    
    # 1. Try direct json parse
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # 2. Extract ```json ... ``` blocks
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 3. Find first '{' and last '}'
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        candidate = text[first_brace:last_brace + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            # Simple cleanup common for local LLM output (trailing commas)
            cleaned = re.sub(r",\s*([\]}])", r"\1", candidate)
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass

    logger.warning(f"Could not parse JSON from response string: {text[:200]}...")
    return {}
