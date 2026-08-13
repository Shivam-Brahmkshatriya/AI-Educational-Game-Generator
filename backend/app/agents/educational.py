import logging
from typing import List
from app.agents.base import call_ollama

logger = logging.getLogger(__name__)

async def run_educational_agent(topic: str, research_facts: List[str]) -> str:
    """
    Embeds learning objectives directly into the gameplay mechanics.
    """
    facts_str = "\n".join([f"- {f}" for f in research_facts])
    prompt = f"""
You are the Educational Integration Specialist Agent.
Topic: "{topic}"
Facts to Embed:
{facts_str}

Task:
Describe how each fact is directly tested or applied in gameplay (NOT just static quiz popups!).
Examples:
- "Catching items labeled with correct fact increases multiplier; catching false items damages health."
- "Solving problem unlocks super boost engine."
- "Player must match fact prompt to correct target zone."

Detail 3 specific gameplay-integrated learning interactions.
"""
    system_prompt = "You integrate pedagogy into game mechanics. Avoid boring quiz popups."
    return await call_ollama(prompt, system_prompt=system_prompt)
