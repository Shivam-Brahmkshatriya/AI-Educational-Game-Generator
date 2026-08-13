import logging
import json
from typing import Dict, Any, Tuple
from app.agents.base import call_ollama, extract_json

logger = logging.getLogger(__name__)

async def run_critic_agent(gdd: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Evaluates GDD against quality guidelines and negative constraints.
    Enforces genre diversity and rejects boring/generic templates.
    """
    gdd_str = json.dumps(gdd, indent=2)
    prompt = f"""
You are the Game Design Quality & Pedagogy Critic.
Evaluate this Game Design Document (GDD):

{gdd_str}

NEGATIVE CONSTRAINTS (REJECT IMMEDIATELY if any apply):
1. REJECT if the game is a generic falling-object catcher ("move bucket left/right to catch items").
2. REJECT if the game is a static linear flashcard deck.
3. REJECT if controls or core mechanics are vague.

MUST APPROVE IF ANY OF THESE GENRES ARE USED:
- Grid / Board / Turn-Based Game (e.g. 3x3 Tic-Tac-Toe, Matrix Board, Puzzle Grid)
- Maze & Dungeon Explorer (2D maze navigation, collecting gems, dodging wall traps)
- Space / Defense Shooter (2D ship/turret shooting target nodes)
- Physics Slingshot / Trajectory Launcher (Drag and release launcher)
- Gravity Runner / Platformer (Invert gravity up/down over spikes)
- High-Speed Slalom / Vehicle Dodger (3-lane vehicle controls)

Output EXACTLY JSON:
```json
{{
  "approved": true,
  "feedback": "Reason for approval or instructions for rewrite."
}}
```
"""
    system_prompt = "You evaluate game design documents. Accept Grid, Board, Maze, Shooter, Runner, Slingshot, and Slalom genres. Return JSON only."
    
    response = await call_ollama(prompt, system_prompt=system_prompt, json_mode=True)
    parsed = extract_json(response)
    
    approved = parsed.get("approved", True)
    feedback = parsed.get("feedback", "GDD meets quality standards.")
    
    logger.info(f"Critic Agent evaluation: Approved={approved}, Feedback='{feedback[:100]}'")
    return approved, feedback
