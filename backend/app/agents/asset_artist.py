import logging
from typing import Dict, Any
from app.agents.base import call_ollama, extract_json

logger = logging.getLogger(__name__)

async def run_asset_artist(gdd: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates procedural graphics specifications, vector shape maps, and color schemes for Phaser 3 runtime rendering.
    """
    theme = gdd.get("visual_theme", {})
    prompt = f"""
You are the Technical Asset Artist for 2D Procedural HTML5 Games.
Game Title: {gdd.get("game_title")}
Visual Theme: {theme}

Design procedural visual parameters for Phaser 3 (vector shapes, colors, particles, icons).

Output EXACTLY JSON:
```json
{{
  "colors": {{
    "background": "#0f172a",
    "player": "#38bdf8",
    "target_correct": "#4ade80",
    "target_hazard": "#f87171",
    "ui_text": "#ffffff",
    "accent_glow": "#a855f7"
  }},
  "sprites": {{
    "player": {{ "type": "circle", "radius": 24, "fill": "#38bdf8", "stroke": "#ffffff" }},
    "target_correct": {{ "type": "star", "radius": 20, "fill": "#4ade80" }},
    "target_hazard": {{ "type": "triangle", "size": 30, "fill": "#f87171" }}
  }},
  "particles": {{
    "collect_effect": {{ "color": "#4ade80", "speed": 150, "scale": 0.5 }},
    "damage_effect": {{ "color": "#f87171", "speed": 200, "scale": 0.6 }}
  }}
}}
```
"""
    system_prompt = "You provide vector asset definitions in JSON format."
    
    response = await call_ollama(prompt, system_prompt=system_prompt, json_mode=True)
    palette = extract_json(response)
    
    if not palette or "colors" not in palette:
        palette = {
            "colors": {
                "background": "#0d1117",
                "player": "#00f0ff",
                "target_correct": "#39ff14",
                "target_hazard": "#ff0055",
                "ui_text": "#ffffff",
                "accent_glow": "#7928ca"
            },
            "sprites": {
                "player": { "type": "circle", "radius": 22, "fill": "#00f0ff", "stroke": "#ffffff" },
                "target_correct": { "type": "circle", "radius": 18, "fill": "#39ff14" },
                "target_hazard": { "type": "square", "size": 28, "fill": "#ff0055" }
            },
            "particles": {
                "collect_effect": { "color": "#39ff14", "speed": 120, "scale": 0.5 }
            }
        }
        
    logger.info("Asset Artist generated procedural sprite specs.")
    return palette
