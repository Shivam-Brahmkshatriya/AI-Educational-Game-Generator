import logging
from app.agents.base import call_ollama

logger = logging.getLogger(__name__)

async def run_narrative_agent(topic: str) -> str:
    """
    Creates engaging theme, setting, and character concept.
    """
    prompt = f"""
You are the Creative Narrative & World Builder Agent.
Educational Topic: "{topic}"

Design a vibrant, engaging theme and world for a 2D retro arcade game.
Include:
- World Setting (e.g. Cyberpunk Lab, Cosmic Galaxy, Underwater Coral Realm, Ancient Temple)
- Hero Character (e.g. Astro-Cat, Robo-Cadet, Sparky the Firefly, Pixel Knight)
- Antagonist / Hazard Obstacles
- Color Palette Vibe (e.g. Neon Cyberpunk, Pastel Crystal, Dark Synthwave, Forest Emerald)
"""
    system_prompt = "You are an imaginative narrative designer. Keep it engaging for students."
    return await call_ollama(prompt, system_prompt=system_prompt)
