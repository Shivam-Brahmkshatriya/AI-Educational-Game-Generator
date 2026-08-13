import logging
import random
from typing import List, Optional
from app.agents.base import call_ollama

logger = logging.getLogger(__name__)

GAME_GENRES = [
    {
        "name": "Grid / Board / Turn-Based Game",
        "description": "3x3 or 4x4 interactive clickable grid (Tic-Tac-Toe, Matrix Match, Grid Puzzle) where players solve concept challenges to claim cells."
    },
    {
        "name": "Maze & Dungeon Explorer",
        "description": "2D tile maze where the player uses Arrow keys to navigate corridors, collect knowledge gems, dodge wall hazards, and reach the exit portal."
    },
    {
        "name": "Arcade Space / Defense Shooter",
        "description": "2D ship/turret shooting laser pulses at incoming hazards and target nodes. Move left/right, press Space to fire."
    },
    {
        "name": "Physics Slingshot / Trajectory Launcher",
        "description": "Drag and release launcher with angle/power trajectory lines to hit target structures containing educational concepts."
    },
    {
        "name": "Gravity-Flipping Runner Platformer",
        "description": "Character runs forward automatically. Tap Space to invert gravity (ceiling/floor), dodge spikes, collect energy orbs, and pass through gate locks."
    },
    {
        "name": "High-Speed Slalom / Vehicle Dodger",
        "description": "Drive a futuristic hover-car through 3-4 highway lanes. Steer left/right to hit speed-boost facts while dodging obstacles."
    }
]

async def run_mechanic_agent(topic: str, research_facts: List[str], genre_override: Optional[str] = None) -> str:
    """
    Brainstorms dynamic 2D Phaser.js mechanics tailored to a chosen arcade/board genre.
    Respects manual genre_override if provided.
    """
    topic_lower = topic.lower()
    genre = None

    if genre_override and genre_override != "Auto-Detect (AI Managed)":
        for g in GAME_GENRES:
            if g["name"].lower() in genre_override.lower() or genre_override.lower() in g["name"].lower():
                genre = g
                break

    if not genre:
        # Auto-detect genre based on topic
        if any(k in topic_lower for k in ["tic", "tac", "toe", "grid", "board", "matrix", "turn"]):
            genre = GAME_GENRES[0] # Grid / Board
        elif any(k in topic_lower for k in ["maze", "labyrinth", "dungeon", "explore"]):
            genre = GAME_GENRES[1] # Maze Explorer
        else:
            genre = random.choice(GAME_GENRES[2:])

    facts_str = "\n".join([f"- {f}" for f in research_facts])
    
    prompt = f"""
You are an award-winning Senior Gameplay Mechanic Designer.
Educational Topic: "{topic}"
Key Facts to Teach:
{facts_str}

SELECTED GAME GENRE: {genre['name']}
Genre Style Description: {genre['description']}

Propose a high-octane 2D game mechanic loop for this genre.
Your proposal MUST explicitly explain:
1. Player Controls & Core Movement matching the genre ({genre['name']}).
2. How facts from "{topic}" trigger active gameplay rewards (e.g. ammo boost, speed dash, grid claim, shield, score multiplier).
3. Primary win and loss conditions.

Keep it detailed, concise, and focused strictly on active gameplay mechanics.
"""
    system_prompt = "You design novel 2D game mechanics matching specific arcade genres. Return concise text."
    
    response = await call_ollama(prompt, system_prompt=system_prompt)
    logger.info(f"Mechanics Agent generated proposal for topic '{topic}' using genre '{genre['name']}'")
    return response
