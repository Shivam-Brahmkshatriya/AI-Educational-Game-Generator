import logging
from typing import Dict, Any, List, Optional
from app.agents.base import call_ollama, extract_json

logger = logging.getLogger(__name__)

async def run_master_designer(
    topic: str,
    research_facts: List[str],
    mechanics_idea: str,
    narrative_idea: str,
    educational_idea: str,
    genre_override: Optional[str] = None,
    feedback: str = ""
) -> Dict[str, Any]:
    """
    Synthesizes sub-agent ideas into a rigid Game Design Document (GDD) with specific genre classification.
    Respects genre_override from state.
    """
    facts_str = "\n".join([f"- {f}" for f in research_facts])
    feedback_context = f"\nRejection/User Feedback to Incorporate:\n{feedback}\n" if feedback else ""
    topic_lower = topic.lower()

    default_genre = "Arcade Space / Defense Shooter"
    default_controls = "Left / Right Arrow Keys to steer ship, Spacebar to fire photon lasers."
    default_mechanic = f"Player steers ship and fires lasers at target concept asteroids for {topic}."

    if genre_override and genre_override != "Auto-Detect (AI Managed)":
        default_genre = genre_override
        if "bike" in genre_override.lower() or "rider" in genre_override.lower():
            default_controls = "Left / Right Arrow Keys to switch lanes, Up Arrow for Nitro Boost."
            default_mechanic = "Player rides motorcycle at high speed on a 3-lane highway, collecting energy boost canisters and dodging cones."
        elif "grid" in genre_override.lower() or "board" in genre_override.lower():
            default_controls = "Click grid cells to answer concept questions and claim cells."
            default_mechanic = "Players solve educational questions to claim grid cells in Tic-Tac-Toe turn-based format."
        elif "maze" in genre_override.lower():
            default_controls = "Arrow Keys / WASD to navigate hero through maze corridors."
            default_mechanic = "Player moves hero through tile maze, collecting knowledge gems while dodging wall traps."
    else:
        if any(k in topic_lower for k in ["bike", "motorbike", "rider", "cycle", "motorcycle", "highway"]):
            default_genre = "2D Bike Rider / Motorbike Highway Dodge"
            default_controls = "Left / Right Arrow Keys to switch lanes, Up Arrow for Nitro Boost."
            default_mechanic = "Player rides motorcycle at high speed on a 3-lane highway, collecting energy boost canisters and dodging cones."
        elif any(k in topic_lower for k in ["tic", "tac", "toe", "grid", "board", "turn", "matrix", "puzzle"]):
            default_genre = "Grid / Board / Turn-Based Game"
            default_controls = "Click any 3x3 grid cell to answer questions and place your mark (X or O)."
            default_mechanic = "Players click 3x3 grid cells, solve educational questions, and try to complete 3-in-a-row!"
        elif any(k in topic_lower for k in ["maze", "dungeon", "labyrinth", "explore"]):
            default_genre = "Maze & Dungeon Explorer"
            default_controls = "Arrow Keys / WASD to navigate hero through maze corridors."
            default_mechanic = "Player moves hero through tile maze, collecting knowledge gems while dodging wall traps to reach the exit portal."
        elif any(k in topic_lower for k in ["runner", "platformer", "jump", "gravity"]):
            default_genre = "Gravity-Flipping Runner Platformer"
            default_controls = "Press Spacebar to invert gravity between floor and ceiling."
            default_mechanic = "Player runs continuously, tapping Space to flip gravity over spikes and collect energy orbs."
        elif any(k in topic_lower for k in ["slingshot", "launcher", "catapult", "angle"]):
            default_genre = "Physics Slingshot / Trajectory Launcher"
            default_controls = "Drag mouse pointer backward and release to launch projectile."
            default_mechanic = "Player aims launcher at target block towers embedded with knowledge facts."
        elif any(k in topic_lower for k in ["slalom", "dodger", "race", "car", "drive"]):
            default_genre = "High-Speed Slalom / Vehicle Dodger"
            default_controls = "Left & Right Arrow Keys to switch highway lanes."
            default_mechanic = "Player drives hovercraft through 3 lanes hitting speed boost concept pads."

    prompt = f"""
You are the Master Game Designer & Systems Architect.
Synthesize the specialist sub-agent ideas into a unified, rigid Game Design Document (GDD).

Topic: "{topic}"
Facts:
{facts_str}

Mechanics Proposal:
{mechanics_idea}

Narrative Proposal:
{narrative_idea}

Educational Integration:
{educational_idea}
{feedback_context}

CRITICAL REQUIREMENT:
Output a Game Design Document matching the selected genre EXACTLY: "{default_genre}".

Output EXACTLY a JSON object with this structure:
```json
{{
  "game_title": "{topic} Master",
  "genre": "{default_genre}",
  "tagline": "Short exciting summary",
  "narrative": {{
    "setting": "Description of setting",
    "hero_name": "Hero character name",
    "objective": "Main mission objective"
  }},
  "gameplay_loop": {{
    "controls": "{default_controls}",
    "core_mechanic": "{default_mechanic}",
    "win_condition": "Score >= 1000 or complete run",
    "loss_condition": "Health reaches 0"
  }},
  "educational_rules": [
    {{
      "concept": "Short concept name",
      "correct_answer": "True statement / item",
      "distractors": ["False 1", "False 2"],
      "gameplay_effect": "+200 pts"
    }}
  ],
  "visual_theme": {{
    "background_color": "#090d16",
    "accent_color": "#38bdf8",
    "art_style": "Neon Retro Vector Graphics"
  }}
}}
```
"""
    system_prompt = "You compile specifications into valid JSON. Return valid JSON only."
    
    response = await call_ollama(prompt, system_prompt=system_prompt, json_mode=True)
    gdd = extract_json(response)
    
    if not gdd or "game_title" not in gdd or "genre" not in gdd:
        # Fallback GDD structure using topic-aware genre
        gdd = {
            "game_title": f"{topic} Challenge",
            "genre": default_genre,
            "tagline": f"Master the rules of {topic} in an interactive {default_genre}!",
            "narrative": {
                "setting": "Interactive Learning Environment",
                "hero_name": "Rider / Player 1",
                "objective": f"Solve challenges and master {topic}!"
            },
            "gameplay_loop": {
                "controls": default_controls,
                "core_mechanic": default_mechanic,
                "win_condition": "Complete all levels / win game",
                "loss_condition": "Run out of health"
            },
            "educational_rules": [
                {
                    "concept": f"Fact: {research_facts[0] if research_facts else topic}",
                    "correct_answer": "Correct Answer",
                    "distractors": ["Incorrect 1", "Incorrect 2"],
                    "gameplay_effect": "+200 Points"
                }
            ],
            "visual_theme": {
                "background_color": "#090d16",
                "accent_color": "#38bdf8",
                "art_style": "Neon Vector"
            }
        }

    # Enforce default_genre so LLM cannot hallucinate another genre
    gdd["genre"] = default_genre
        
    logger.info(f"Master Designer compiled GDD: '{gdd.get('game_title')}' (Genre: {gdd.get('genre')})")
    return gdd
