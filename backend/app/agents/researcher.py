import logging
from typing import List, Dict, Any
from duckduckgo_search import DDGS
from app.agents.base import call_ollama, extract_json

logger = logging.getLogger(__name__)

async def run_researcher(topic: str) -> List[str]:
    """
    Performs compound research on the topic using DDGS and distills facts using Ollama Gemma 4.
    """
    logger.info(f"Researcher starting compound search for topic: '{topic}'")
    search_results = []
    
    try:
        ddgs = DDGS()
        # Primary search
        results1 = list(ddgs.text(f"educational facts about {topic} for students", max_results=4))
        for r in results1:
            search_results.append(f"Title: {r.get('title')}\nSnippet: {r.get('body')}")
            
        # Secondary search for specific concepts
        results2 = list(ddgs.text(f"key rules formulas concepts {topic}", max_results=3))
        for r in results2:
            search_results.append(f"Title: {r.get('title')}\nSnippet: {r.get('body')}")
    except Exception as e:
        logger.warning(f"DuckDuckGo search error (falling back to LLM internal knowledge): {e}")

    raw_context = "\n---\n".join(search_results) if search_results else f"Topic: {topic}"

    prompt = f"""
You are an expert Educational Researcher Agent.
Topic to research: "{topic}"

Web Search Results / Context:
{raw_context}

Task:
Extract 3 to 5 core, accurate, and essential educational facts, formulas, or principles about this topic that can be embedded into an interactive 2D HTML5 game.

Format output EXACTLY as a JSON array of strings inside a JSON object:
```json
{{
  "facts": [
    "Fact 1 description...",
    "Fact 2 description...",
    "Fact 3 description...",
    "Fact 4 description..."
  ]
}}
```
"""
    system_prompt = "You are a factual research assistant. Respond strictly in the requested JSON format."
    
    response = await call_ollama(prompt, system_prompt=system_prompt, json_mode=True)
    parsed = extract_json(response)
    facts = parsed.get("facts", [])
    
    if not facts or not isinstance(facts, list):
        # Fallback list if parsing fails
        facts = [
            f"Core principle 1 of {topic}: Fundamental concept definition.",
            f"Core principle 2 of {topic}: Key interactive rule or equation.",
            f"Core principle 3 of {topic}: Practical application and problem solving."
        ]
        
    logger.info(f"Researcher extracted {len(facts)} facts for '{topic}'")
    return facts
