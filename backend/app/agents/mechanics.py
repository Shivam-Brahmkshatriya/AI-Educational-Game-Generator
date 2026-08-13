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
    },
    {
        "name": "Arcade Space / Defense Shooter",
        "description": "2D ship/turret shooting laser pulses at incoming hazards and target nodes. Move left/right, press Space to fire."
    },
    {
        "name": "Brick Breaker / Arkanoid Paddle Physics",
        "description": "Control a horizontal paddle to bounce a ball, destroying educational bricks, collecting power-ups, and unlocking level doors."
    },
    {
        "name": "2D Side-Scrolling Jump & Run Platformer",
        "description": "Classic 2D platformer with jumping over pits, stomping target enemies, collecting coins, and reaching the finish flag."
    },
    {
        "name": "Bubble Shooter / Match-3 Cannon",
        "description": "Aim and fire colored concept spheres at matching clusters to trigger chain reactions and clear the board."
    },
    {
        "name": "Tower Defense & Base Guardian",
        "description": "Place strategic defensive turrets along a path to stop incoming wave creeps while answering trivia to earn gold."
    },
    {
        "name": "Top-Down Retro RPG Quest & Battle",
        "description": "Explore an 8-bit overworld map, talk to wizard NPCs, battle wild boss encounters using concept magic spells."
    },
    {
        "name": "Card Match & Memory Concentration",
        "description": "Flip over hidden cards to pair matching educational terms, formulas, and visual diagrams."
    },
    {
        "name": "Word Scramble & Vocabulary Solver",
        "description": "Unscramble missing educational terms and formula keywords letter-by-letter before the timer expires."
    }
]

async def run_mechanic_agent(topic: str, research_facts: List[str], genre_override: Optional[str] = None) -> str:
    """
    Brainstorms dynamic 2D Phaser.js mechanics tailored to a chosen arcade/board/RPG genre.
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
            genre = {"name": genre_override, "description": f"Custom player genre: {genre_override}"}
    else:
        if any(k in topic_lower for k in ["brick", "breaker", "arkanoid", "bounce", "paddle", "pong"]):
            genre = GAME_GENRES[6]
        elif any(k in topic_lower for k in ["bubble", "match", "cannon", "cluster"]):
            genre = GAME_GENRES[8]
        elif any(k in topic_lower for k in ["tower", "defense", "turret", "wave", "base"]):
            genre = GAME_GENRES[9]
        elif any(k in topic_lower for k in ["rpg", "quest", "wizard", "hero", "battle", "retro"]):
            genre = GAME_GENRES[10]
        elif any(k in topic_lower for k in ["memory", "card", "flip", "pair", "matching"]):
            genre = GAME_GENRES[11]
        elif any(k in topic_lower for k in ["word", "scramble", "spelling", "hang", "vocab"]):
            genre = GAME_GENRES[12]
        elif any(k in topic_lower for k in ["mario", "platform", "jump", "sonic", "side"]):
            genre = GAME_GENRES[7]
        elif any(k in topic_lower for k in ["tic", "tac", "toe", "grid", "board", "puzzle", "matrix"]):
            genre = GAME_GENRES[0]
        elif any(k in topic_lower for k in ["maze", "dungeon", "labyrinth", "explore"]):
            genre = GAME_GENRES[1]
        elif any(k in topic_lower for k in ["slingshot", "launch", "angle", "catapult", "physics"]):
            genre = GAME_GENRES[2]
        elif any(k in topic_lower for k in ["runner", "gravity", "flip"]):
            genre = GAME_GENRES[3]
        elif any(k in topic_lower for k in ["slalom", "dodger", "race", "car", "drive"]):
            genre = GAME_GENRES[4]
        elif any(k in topic_lower for k in ["space", "ship", "shoot", "defend", "laser"]):
            genre = GAME_GENRES[5]
        else:
            genre = random.choice(GAME_GENRES)

    facts_summary = "\n".join([f"- {f}" for f in research_facts])

    prompt = f"""
You are the Lead Gameplay Mechanics Designer.
Create a unique 2D gameplay mechanic spec for an educational game about: "{topic}".

SPECIFIED GAME GENRE: {genre['name']}
Genre Description: {genre['description']}

Fact Database:
{facts_summary}

STRICT REQUIREMENTS FOR THIS GENRE ({genre['name']}):
1. THE GAMEPLAY MUST ACCURATELY REFLECT THIS GENRE:
   - If Brick Breaker: Horizontal paddle bouncing balls to break concept bricks!
   - If Side-Scrolling Platformer: Jumping over gaps, collecting coins, reaching the flag!
   - If RPG Quest: 2D tile map exploration with wizard NPCs and concept spell battles!
   - If Tower Defense: Strategic turret placement along a path to destroy wave creeps!
   - If Grid/Board: Must use clickable grid cells and turn-based logic!
   - If Maze: Must use a tile grid maze with player movement and collectible gems!
2. Do NOT default to falling objects!
3. Define player controls clearly (Arrow keys, Spacebar, Mouse clicks).
4. Specify educational interaction (e.g. collecting facts boosts speed/score, wrong obstacles deduct health).

Format response as JSON:
{{
  "genre": "{genre['name']}",
  "player_controls": "...",
  "primary_mechanic": "...",
  "educational_win_condition": "...",
  "visual_theme": "..."
}}
"""
    system_prompt = "You are a master game designer specializing in dynamic HTML5 Phaser 3 game mechanics."
    return await call_ollama(prompt, system_prompt=system_prompt, temperature=0.2)
