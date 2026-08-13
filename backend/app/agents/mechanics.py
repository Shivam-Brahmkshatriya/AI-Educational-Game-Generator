import logging
import random
from typing import List
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

async def run_mechanic_agent(topic: str, research_facts: List[str]) -> str:
    """
    Brainstorms dynamic 2D Phaser.js mechanics tailored to a chosen arcade/board genre.
    """
    topic_lower = topic.lower()
    
    # Auto-detect specific genre request from topic name if present
    if any(k in topic_lower for k in ["tic", "tac", "toe", "grid", "board", "matrix", "turn"]):
        genre = GAME_GENRES[0] # Grid / Board
    elif any(k in topic_lower for k in ["maze", "labyrinth", "dungeon", "explore"]):
        genre = GAME_GENRES[1] # Maze Explorer
    else:
        # Otherwise pick a dynamic genre to guarantee variety
        genre = random.choice(GAME_GENRES[2:])

    facts_str = "\n".join([f"- {f}" for f in research_facts])
    
    prompt = f"""
You are an award-winning Senior Gameplay Mechanic Designer.
Educational Topic: "{topic}"
Key Facts to Teach:
{facts_str}

SELECTED GAME GENRE: {genre['name']}
Genre Style Description: {genre['description']}

Task:
Design a unique 2D gameplay loop in Phaser.js using the "{genre['name']}" format.

STRICT RULES:
1. DO NOT use generic falling-object catcher templates.
2. If the genre is Grid/Board (e.g. Tic-Tac-Toe), design an interactive 3x3 clickable grid turn game!
3. If the genre is Maze, design a 2D tile explorer game!
4. Ensure player controls are explicit and responsive.

Detail:
- Selected Genre & Title Concept
- Exact Player Controls & Actions
- Core Gameplay Loop & Win/Loss Conditions
- How the educational facts trigger dynamic gameplay rewards.
"""
    system_prompt = f"You design creative 2D games in the {genre['name']} genre."
    return await call_ollama(prompt, system_prompt=system_prompt)
