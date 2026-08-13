import logging
import re
import json
from typing import Dict, Any
from app.agents.base import call_ollama

logger = logging.getLogger(__name__)

async def run_lead_developer(
    gdd: Dict[str, Any],
    asset_palette: Dict[str, Any],
    qa_report: Dict[str, Any] = None
) -> str:
    """
    Authors a complete, self-contained single-file Phaser.js HTML5 game matching the GDD genre & mechanics.
    Injects WebAudio procedural sound synthesis, particle effects, and post-game educational analytics.
    """
    gdd_str = json.dumps(gdd, indent=2)
    palette_str = json.dumps(asset_palette, indent=2)
    genre = gdd.get("genre", "Space Shooter")
    title = gdd.get("game_title", "Educational Game")
    
    qa_fix_instruction = ""
    if qa_report and not qa_report.get("passed", True):
        errors = qa_report.get("errors", [])
        qa_fix_instruction = f"""
CRITICAL FIX REQUIRED (PREVIOUS TEST FAILED):
The previous code execution encountered the following browser console/runtime errors:
{json.dumps(errors, indent=2)}

You MUST fix these exact bugs in the Phaser code. Ensure all variables are defined, physics bodies are added correctly, and no undefined methods are invoked.
"""

    prompt = f"""
You are the Senior Lead Developer specializing in 2D HTML5 Phaser 3 Games.
Author a COMPLETE, standalone, fully-functional single-file HTML document `index.html`.

Game Title: "{title}"
Specified Genre: "{genre}"

Game Specifications (GDD):
{gdd_str}

Asset Palette & Visual Spec:
{palette_str}
{qa_fix_instruction}

STRICT REQUIREMENTS:
1. Import Phaser 3 script tag: `<script src="https://cdn.jsdelivr.net/npm/phaser@3.80.0/dist/phaser.min.js"></script>`
2. IMPLEMENT THE EXACT GENRE AND MECHANICS SPECIFIED IN THE GDD:
   - If Tic-Tac-Toe / Grid / Board: Create a 3x3 interactive clickable grid with X and O logic, turn switching, and educational trivia before placing marks!
   - If Bike Rider / Motorbike Highway: Create a high-speed motorcycle rider on a 3-lane highway with Left/Right lane switching, wheelie boost, energy pickups, and road hazards!
   - If Maze / Labyrinth / Dungeon: Create a maze grid with player movement (Arrow keys/WASD), collectible facts, wall colliders, and an exit portal!
   - If Shooter: Create a space/turret shooter.
   - If Runner / Platformer: Create a gravity runner or jumping platformer.
   - If Slingshot / Physics: Create drag-and-launch physics.
3. DO NOT default to a falling object catcher or shooter if the genre is a bike rider, board game, grid puzzle, maze, or runner!
4. Use inline JavaScript inside a `<script>` tag. No external assets/images! Use Phaser procedural graphics or styled HTML/Canvas buttons.
5. Ingest WebAudio procedural SFX for sound feedback (`playSound('collect')`, `playSound('hit')`, `playSound('win')`, `playSound('click')`).

OUTPUT FORMAT:
Return valid HTML. Start your response immediately with `<!DOCTYPE html>` or put the HTML code inside ````html ... ```` code blocks.
"""

    system_prompt = "You are an expert Phaser 3 developer. Author valid, bug-free, complete single-file HTML5 games with inline JS, WebAudio SFX, and Phaser physics."
    
    response = await call_ollama(prompt, system_prompt=system_prompt, temperature=0.1)
    html_code = extract_html_code(response)
    
    if not html_code or len(html_code) < 300:
        logger.warning(f"LLM response did not contain complete HTML. Generating robust genre template for genre: '{genre}'...")
        html_code = generate_dynamic_genre_phaser_game(gdd, asset_palette)

    logger.info(f"Lead Developer generated {len(html_code)} bytes of HTML5 Phaser code for genre '{genre}'.")
    return html_code


def extract_html_code(response_text: str) -> str:
    if not response_text:
        return ""
    match = re.search(r"```html\s*(.*?)\s*```", response_text, re.DOTALL | re.IGNORECASE)
    if match and len(match.group(1).strip()) > 200:
        return match.group(1).strip()
    match = re.search(r"```\s*(<!DOCTYPE html>.*?</html>)\s*```", response_text, re.DOTALL | re.IGNORECASE)
    if match and len(match.group(1).strip()) > 200:
        return match.group(1).strip()
    match = re.search(r"(<!DOCTYPE html>.*?</html>)", response_text, re.DOTALL | re.IGNORECASE)
    if match and len(match.group(1).strip()) > 200:
        return match.group(1).strip()
    match = re.search(r"(<html.*?>.*?</html>)", response_text, re.DOTALL | re.IGNORECASE)
    if match and len(match.group(1).strip()) > 200:
        return "<!DOCTYPE html>\n" + match.group(1).strip()
    return ""


def generate_dynamic_genre_phaser_game(gdd: Dict[str, Any], palette: Dict[str, Any]) -> str:
    genre_str = str(gdd.get("genre", "")).lower()
    title_str = str(gdd.get("game_title", "")).lower()
    combined_str = f"{genre_str} {title_str}"
    
    if any(k in combined_str for k in ["bike", "motorbike", "rider", "cycle", "motorcycle"]):
        return build_bike_rider_game(gdd, palette)
    elif any(k in combined_str for k in ["tic", "tac", "toe", "grid", "board", "turn", "matrix", "puzzle"]):
        return build_grid_tictactoe_game(gdd, palette)
    elif any(k in combined_str for k in ["maze", "dungeon", "labyrinth", "explore", "quest"]):
        return build_maze_explorer_game(gdd, palette)
    elif any(k in combined_str for k in ["runner", "platformer", "jump", "gravity"]):
        return build_gravity_runner_game(gdd, palette)
    elif any(k in combined_str for k in ["slingshot", "launcher", "catapult", "angle"]):
        return build_slingshot_launcher_game(gdd, palette)
    elif any(k in combined_str for k in ["slalom", "dodger", "race", "car", "drive"]):
        return build_vehicle_slalom_game(gdd, palette)
    else:
        return build_space_shooter_game(gdd, palette)


# ==============================================================================
# GENRE 0: 2D Bike Rider / Motorbike Highway Dodge Game
# ==============================================================================
def build_bike_rider_game(gdd: Dict[str, Any], palette: Dict[str, Any]) -> str:
    title = gdd.get("game_title", "Highway Bike Rider")
    colors = palette.get("colors", {})
    bg_color = colors.get("background", "#090d16")
    bike_color = colors.get("player", "#38bdf8")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{
      margin: 0; padding: 0;
      background-color: {bg_color}; color: #ffffff;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      min-height: 100vh; overflow: hidden;
    }}
    #game-container {{
      border: 3px solid #38bdf8; border-radius: 16px; overflow: hidden;
      box-shadow: 0 0 30px rgba(56,189,248,0.3);
    }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/phaser@3.80.0/dist/phaser.min.js"></script>
</head>
<body>
  <div id="game-container"></div>

  <script>
    function playSound(type) {{
      try {{
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator(); const gain = ctx.createGain();
        osc.connect(gain); gain.connect(ctx.destination); const now = ctx.currentTime;
        if (type === 'rev' || type === 'collect') {{
          osc.type = 'sawtooth'; osc.frequency.setValueAtTime(220, now);
          osc.frequency.exponentialRampToValueAtTime(660, now + 0.15);
          gain.gain.setValueAtTime(0.2, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
          osc.start(now); osc.stop(now + 0.15);
        }} else if (type === 'hit') {{
          osc.type = 'square'; osc.frequency.setValueAtTime(140, now);
          osc.frequency.exponentialRampToValueAtTime(30, now + 0.25);
          gain.gain.setValueAtTime(0.3, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
          osc.start(now); osc.stop(now + 0.25);
        }} else if (type === 'win') {{
          osc.type = 'triangle'; osc.frequency.setValueAtTime(440, now);
          osc.frequency.setValueAtTime(554.37, now + 0.1);
          osc.frequency.setValueAtTime(659.25, now + 0.2);
          gain.gain.setValueAtTime(0.3, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
          osc.start(now); osc.stop(now + 0.4);
        }}
      }} catch(e) {{}}
    }}

    const config = {{
      type: Phaser.AUTO, width: 800, height: 600, parent: 'game-container', backgroundColor: '{bg_color}',
      physics: {{ default: 'arcade', arcade: {{ gravity: {{ y: 0 }}, debug: false }} }},
      scene: {{ preload: preload, create: create, update: update }}
    }};

    let bike, boostItems, hazards, cursors, lanes = [250, 400, 550], currentLane = 1;
    let score = 0, speedKm = 120, health = 3, gameActive = true;
    let scoreText, speedText, healthText, statusText;

    const game = new Phaser.Game(config);

    function preload() {{
      let g = this.add.graphics();
      // Draw Bike graphic
      g.fillStyle(parseInt("{bike_color}".replace("#","0x")), 1);
      g.fillRect(12, 0, 16, 50); // Body
      g.fillStyle(0x000000, 1);
      g.fillRect(8, 5, 24, 8); // Front Wheel Handlebars
      g.fillRect(8, 38, 24, 8); // Rear Wheel
      g.fillStyle(0xfbbf24, 1);
      g.fillCircle(20, 2, 4); // Headlight
      g.generateTexture('bike_tex', 40, 50); g.clear();

      // Energy Boost Canister
      g.fillStyle(0x4ade80, 1); g.fillRoundedRect(0, 0, 30, 40, 8);
      g.fillStyle(0xffffff, 1); g.fillRect(10, 8, 10, 24);
      g.generateTexture('boost_tex', 30, 40); g.clear();

      // Traffic Hazard Cone
      g.fillStyle(0xf87171, 1); g.fillTriangle(20, 0, 0, 40, 40, 40);
      g.fillStyle(0xffffff, 1); g.fillRect(8, 24, 24, 6);
      g.generateTexture('cone_tex', 40, 40); g.destroy();
    }}

    function create() {{
      // Highway Lane Marking Lines
      let g = this.add.graphics();
      g.lineStyle(4, 0x334155, 1);
      g.lineBetween(325, 0, 325, 600);
      g.lineBetween(475, 0, 475, 600);

      // Yellow Shoulders
      g.lineStyle(6, 0xfbbf24, 0.8);
      g.lineBetween(175, 0, 175, 600);
      g.lineBetween(625, 0, 625, 600);

      bike = this.physics.add.sprite(lanes[currentLane], 500, 'bike_tex');
      cursors = this.input.keyboard.createCursorKeys();
      boostItems = this.physics.add.group();
      hazards = this.physics.add.group();

      scoreText = this.add.text(20, 20, 'Distance Score: 0', {{ fontSize: '20px', fill: '#4ade80', fontWeight: 'bold' }});
      speedText = this.add.text(20, 50, 'Speed: 120 km/h', {{ fontSize: '18px', fill: '#38bdf8' }});
      healthText = this.add.text(620, 20, 'Bike Health: 🏍️🏍️🏍️', {{ fontSize: '18px', fill: '#f87171' }});
      statusText = this.add.text(400, 570, 'STEER WITH LEFT / RIGHT ARROWS | PRESS UP FOR NITRO BOOST', {{ fontSize: '13px', fill: '#94a3b8' }}).setOrigin(0.5);

      this.time.addEvent({{ delay: 900, callback: spawnHighwayItems, callbackScope: this, loop: true }});

      this.physics.add.overlap(bike, boostItems, collectBoost, null, this);
      this.physics.add.overlap(bike, hazards, hitCone, null, this);
    }}

    function update() {{
      if (!gameActive) return;

      if (Phaser.Input.Keyboard.JustDown(cursors.left) && currentLane > 0) {{
        currentLane--;
        bike.x = lanes[currentLane];
        playSound('rev');
      }} else if (Phaser.Input.Keyboard.JustDown(cursors.right) && currentLane < 2) {{
        currentLane++;
        bike.x = lanes[currentLane];
        playSound('rev');
      }}

      if (cursors.up.isDown) {{
        speedKm = 180;
        bike.y = 470;
      }} else {{
        speedKm = 120;
        bike.y = 500;
      }}

      score += Math.round(speedKm / 40);
      scoreText.setText('Distance Score: ' + score);
      speedText.setText('Speed: ' + speedKm + ' km/h');
    }}

    function spawnHighwayItems() {{
      if (!gameActive) return;
      let laneIdx = Phaser.Math.Between(0, 2);
      let fallSpeed = speedKm * 2.5;
      if (Math.random() > 0.4) {{
        let boost = boostItems.create(lanes[laneIdx], -40, 'boost_tex');
        boost.setVelocityY(fallSpeed);
      }} else {{
        let cone = hazards.create(lanes[laneIdx], -40, 'cone_tex');
        cone.setVelocityY(fallSpeed);
      }}
    }}

    function collectBoost(bike, boost) {{
      boost.destroy();
      playSound('collect');
      score += 250;
      scoreText.setText('Distance Score: ' + score);
    }}

    function hitCone(bike, cone) {{
      cone.destroy();
      playSound('hit');
      health--;
      if (health <= 0) {{
        healthText.setText('Bike Health: 💥 CRASHED');
        gameActive = false;
        bike.setTint(0xff0000);
        this.add.text(400, 300, 'GAME OVER\\nBike Highway Crash!', {{ fontSize: '32px', fill: '#f87171', align: 'center', fontWeight: 'bold' }}).setOrigin(0.5);
      }} else {{
        healthText.setText('Bike Health: ' + '🏍️'.repeat(health));
      }}
    }}
  </script>
</body>
</html>"""


# ==============================================================================
# GENRE 1: Grid / Tic-Tac-Toe Interactive Educational Board Game
# ==============================================================================
def build_grid_tictactoe_game(gdd: Dict[str, Any], palette: Dict[str, Any]) -> str:
    title = gdd.get("game_title", "Educational Tic-Tac-Toe")
    colors = palette.get("colors", {})
    bg_color = colors.get("background", "#0f172a")
    edu_rules = gdd.get("educational_rules", [])
    
    concept_q = edu_rules[0].get("concept", "Is this concept rule correct?") if edu_rules else "Educational Challenge"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{
      margin: 0; padding: 0;
      background-color: {bg_color}; color: #ffffff;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      min-height: 100vh; overflow: hidden;
    }}
    h1 {{ color: #38bdf8; margin-bottom: 5px; font-size: 1.8rem; text-shadow: 0 0 10px rgba(56,189,248,0.5); }}
    p.subtitle {{ color: #94a3b8; margin-top: 0; margin-bottom: 20px; font-size: 0.9rem; }}
    
    #board {{
      display: grid;
      grid-template-columns: repeat(3, 110px);
      grid-template-rows: repeat(3, 110px);
      gap: 12px;
      background: #1e293b;
      padding: 16px;
      border-radius: 16px;
      box-shadow: 0 15px 35px rgba(0,0,0,0.6), 0 0 20px rgba(56,189,248,0.2);
      border: 2px solid rgba(56,189,248,0.3);
    }}
    .cell {{
      background: #0f172a;
      border: 2px solid rgba(255,255,255,0.1);
      border-radius: 12px;
      display: flex; align-items: center; justify-content: center;
      font-size: 3rem; font-weight: 800; cursor: pointer;
      transition: all 0.2s ease;
      user-select: none;
    }}
    .cell:hover {{
      background: #1e293b;
      border-color: #38bdf8;
      transform: scale(1.04);
    }}
    .cell.x {{ color: #38bdf8; text-shadow: 0 0 12px #38bdf8; }}
    .cell.o {{ color: #f87171; text-shadow: 0 0 12px #f87171; }}
    
    #status {{
      margin-top: 20px; font-size: 1.2rem; font-weight: 600; color: #4ade80; text-align: center;
    }}
    #quiz-modal, #analytics-modal {{
      display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(5,8,15,0.85); backdrop-filter: blur(8px);
      align-items: center; justify-content: center; z-index: 100;
    }}
    .modal-card {{
      background: #0f172a; border: 2px solid #38bdf8; border-radius: 16px;
      padding: 24px; max-width: 440px; text-align: center; box-shadow: 0 0 30px rgba(56,189,248,0.3);
    }}
    .btn {{
      padding: 10px 20px; background: #38bdf8; border: none; color: #000;
      font-weight: 700; border-radius: 8px; cursor: pointer; margin: 8px;
    }}
    .btn:hover {{ background: #7dd3fc; }}
  </style>
</head>
<body>

  <h1>{title}</h1>
  <p class="subtitle">Solve educational questions to claim grid cells & unlock victory!</p>

  <div id="board">
    <div class="cell" onclick="handleCellClick(0)"></div>
    <div class="cell" onclick="handleCellClick(1)"></div>
    <div class="cell" onclick="handleCellClick(2)"></div>
    <div class="cell" onclick="handleCellClick(3)"></div>
    <div class="cell" onclick="handleCellClick(4)"></div>
    <div class="cell" onclick="handleCellClick(5)"></div>
    <div class="cell" onclick="handleCellClick(6)"></div>
    <div class="cell" onclick="handleCellClick(7)"></div>
    <div class="cell" onclick="handleCellClick(8)"></div>
  </div>

  <div id="status">Player X's Turn - Click any cell to solve!</div>

  <div id="quiz-modal">
    <div class="modal-card">
      <h3 style="color:#38bdf8; margin-top:0;">Educational Concept Challenge</h3>
      <p id="quiz-question" style="font-size:0.95rem; color:#cbd5e1;"></p>
      <button class="btn" onclick="submitAnswer(true)" id="ans-true">A) Correct Concept</button>
      <button class="btn" style="background:#f87171;" onclick="submitAnswer(false)">B) Incorrect Concept</button>
    </div>
  </div>

  <div id="analytics-modal">
    <div class="modal-card" style="border-color:#4ade80;">
      <h2 style="color:#4ade80; margin-top:0;">🎓 Mastery Analytics Report</h2>
      <p style="color:#cbd5e1;">Game Session Complete!</p>
      <div style="text-align:left; background:#1e293b; padding:15px; border-radius:10px; margin:15px 0;">
        <p><strong>Concepts Solved:</strong> <span id="stat-solved">0</span></p>
        <p><strong>Accuracy Rating:</strong> <span id="stat-accuracy">100%</span></p>
        <p><strong>Earned Badge:</strong> 🏆 <span id="stat-badge">Master Strategist</span></p>
      </div>
      <button class="btn" onclick="location.reload()">Play Again</button>
    </div>
  </div>

  <script>
    function playSound(type) {{
      try {{
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator(); const gain = ctx.createGain();
        osc.connect(gain); gain.connect(ctx.destination); const now = ctx.currentTime;
        if (type === 'click' || type === 'collect') {{
          osc.type = 'sine'; osc.frequency.setValueAtTime(523.25, now); osc.frequency.setValueAtTime(659.25, now + 0.08);
          gain.gain.setValueAtTime(0.2, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
          osc.start(now); osc.stop(now + 0.2);
        }} else if (type === 'hit') {{
          osc.type = 'square'; osc.frequency.setValueAtTime(160, now); osc.frequency.exponentialRampToValueAtTime(40, now + 0.2);
          gain.gain.setValueAtTime(0.3, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
          osc.start(now); osc.stop(now + 0.2);
        }} else if (type === 'win') {{
          osc.type = 'triangle'; osc.frequency.setValueAtTime(440, now); osc.frequency.setValueAtTime(659.25, now + 0.2);
          gain.gain.setValueAtTime(0.3, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
          osc.start(now); osc.stop(now + 0.4);
        }}
      }} catch(e) {{}}
    }}

    let boardState = Array(9).fill(null);
    let currentPlayer = 'X';
    let selectedCellIndex = null;
    let gameActive = true;
    let totalAttempts = 0, correctAttempts = 0;

    const questions = [
      "{concept_q[:80]}",
      "True or False: Mastering key concepts helps win games!",
      "Concept Check: Does this rule apply correctly?"
    ];

    function handleCellClick(index) {{
      if (!gameActive || boardState[index] !== null) return;
      playSound('click');
      selectedCellIndex = index;
      document.getElementById('quiz-question').innerText = questions[index % questions.length];
      document.getElementById('quiz-modal').style.display = 'flex';
    }}

    function submitAnswer(isCorrect) {{
      totalAttempts++;
      document.getElementById('quiz-modal').style.display = 'none';
      if (isCorrect) {{
        correctAttempts++;
        playSound('collect');
        boardState[selectedCellIndex] = currentPlayer;
        const cells = document.querySelectorAll('.cell');
        cells[selectedCellIndex].innerText = currentPlayer;
        cells[selectedCellIndex].classList.add(currentPlayer.toLowerCase());
        
        if (checkWin()) {{
          playSound('win');
          document.getElementById('status').innerText = '🎉 Player ' + currentPlayer + ' Wins!';
          gameActive = false;
          showAnalytics();
        }} else if (boardState.every(c => c !== null)) {{
          playSound('win');
          document.getElementById('status').innerText = '🤝 Draw Game!';
          gameActive = false;
          showAnalytics();
        }} else {{
          currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
          document.getElementById('status').innerText = "Player " + currentPlayer + "'s Turn";
          if (currentPlayer === 'O' && gameActive) {{
            setTimeout(botTurn, 600);
          }}
        }}
      }} else {{
        playSound('hit');
        document.getElementById('status').innerText = '❌ Incorrect answer! Turn lost.';
        currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
        if (currentPlayer === 'O' && gameActive) {{
          setTimeout(botTurn, 600);
        }}
      }}
    }}

    function botTurn() {{
      const emptyIndices = boardState.map((v, i) => v === null ? i : null).filter(v => v !== null);
      if (emptyIndices.length > 0 && gameActive) {{
        const choice = emptyIndices[Math.floor(Math.random() * emptyIndices.length)];
        boardState[choice] = 'O';
        const cells = document.querySelectorAll('.cell');
        cells[choice].innerText = 'O';
        cells[choice].classList.add('o');
        
        if (checkWin()) {{
          playSound('hit');
          document.getElementById('status').innerText = '🤖 Bot Wins!';
          gameActive = false;
          showAnalytics();
        }} else {{
          currentPlayer = 'X';
          document.getElementById('status').innerText = "Player X's Turn";
        }}
      }}
    }}

    function checkWin() {{
      const wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
      ];
      return wins.some(w => boardState[w[0]] && boardState[w[0]] === boardState[w[1]] && boardState[w[0]] === boardState[w[2]]);
    }}

    function showAnalytics() {{
      const acc = totalAttempts > 0 ? Math.round((correctAttempts / totalAttempts) * 100) : 100;
      document.getElementById('stat-solved').innerText = correctAttempts;
      document.getElementById('stat-accuracy').innerText = acc + '%';
      document.getElementById('stat-badge').innerText = acc >= 80 ? 'Master Strategist 🏆' : 'Concept Apprentice 🎖️';
      setTimeout(() => {{
        document.getElementById('analytics-modal').style.display = 'flex';
      }}, 1000);
    }}
  </script>
</body>
</html>"""


# ==============================================================================
# GENRE 2: Maze / Labyrinth Interactive Dungeon Explorer
# ==============================================================================
def build_maze_explorer_game(gdd: Dict[str, Any], palette: Dict[str, Any]) -> str:
    title = gdd.get("game_title", "Maze Explorer")
    colors = palette.get("colors", {})
    bg_color = colors.get("background", "#090d16")
    player_color = colors.get("player", "#38bdf8")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{ margin: 0; padding: 0; background-color: {bg_color}; color: #fff; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; }}
    #game-container {{ border: 3px solid #38bdf8; border-radius: 12px; overflow: hidden; }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/phaser@3.80.0/dist/phaser.min.js"></script>
</head>
<body>
  <div id="game-container"></div>
  <script>
    function playSound(type) {{
      try {{
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator(); const gain = ctx.createGain();
        osc.connect(gain); gain.connect(ctx.destination); const now = ctx.currentTime;
        if (type === 'collect') {{
          osc.type = 'sine'; osc.frequency.setValueAtTime(523.25, now); osc.frequency.setValueAtTime(659.25, now + 0.08);
          gain.gain.setValueAtTime(0.2, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
          osc.start(now); osc.stop(now + 0.2);
        }} else if (type === 'win') {{
          osc.type = 'triangle'; osc.frequency.setValueAtTime(440, now); osc.frequency.setValueAtTime(659.25, now + 0.2);
          gain.gain.setValueAtTime(0.3, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
          osc.start(now); osc.stop(now + 0.4);
        }}
      }} catch(e) {{}}
    }}

    const config = {{
      type: Phaser.AUTO, width: 800, height: 600, parent: 'game-container', backgroundColor: '{bg_color}',
      physics: {{ default: 'arcade', arcade: {{ gravity: {{ y: 0 }}, debug: false }} }},
      scene: {{ preload: preload, create: create, update: update }}
    }};

    let player, walls, gems, exitPortal, cursors, score = 0, scoreText, statusText;
    let gameActive = true;

    const game = new Phaser.Game(config);

    function preload() {{
      let g = this.add.graphics();
      g.fillStyle(parseInt("{player_color}".replace("#","0x")), 1); g.fillCircle(16, 16, 16);
      g.generateTexture('player_tex', 32, 32); g.clear();

      g.fillStyle(0x334155, 1); g.fillRect(0, 0, 40, 40);
      g.generateTexture('wall_tex', 40, 40); g.clear();

      g.fillStyle(0x4ade80, 1); g.fillCircle(12, 12, 12);
      g.generateTexture('gem_tex', 24, 24); g.clear();

      g.fillStyle(0xc084fc, 1); g.fillRect(0, 0, 40, 40);
      g.generateTexture('portal_tex', 40, 40); g.destroy();
    }}

    function create() {{
      walls = this.physics.add.staticGroup(); gems = this.physics.add.group();

      for (let x = 0; x < 800; x += 40) {{ walls.create(x + 20, 20, 'wall_tex'); walls.create(x + 20, 580, 'wall_tex'); }}
      for (let y = 40; y < 580; y += 40) {{ walls.create(20, y + 20, 'wall_tex'); walls.create(780, y + 20, 'wall_tex'); }}

      let mazeGrid = [[160, 120], [160, 240], [160, 360], [160, 480], [320, 200], [320, 400], [480, 120], [480, 320], [640, 240], [640, 440]];
      mazeGrid.forEach(p => walls.create(p[0], p[1], 'wall_tex'));

      let gemLocs = [[240, 160], [400, 300], [560, 160], [400, 480], [600, 360]];
      gemLocs.forEach(p => gems.create(p[0], p[1], 'gem_tex'));

      exitPortal = this.physics.add.sprite(720, 500, 'portal_tex'); exitPortal.body.allowGravity = false;
      player = this.physics.add.sprite(80, 80, 'player_tex'); player.setCollideWorldBounds(true);

      this.physics.add.collider(player, walls);
      this.physics.add.overlap(player, gems, collectGem, null, this);
      this.physics.add.overlap(player, exitPortal, reachExit, null, this);

      cursors = this.input.keyboard.createCursorKeys();
      scoreText = this.add.text(40, 40, 'Knowledge Gems: 0 / 5', {{ fontSize: '18px', fill: '#4ade80', fontWeight: 'bold' }});
      statusText = this.add.text(400, 560, 'NAVIGATE WITH ARROW KEYS TO COLLECT ALL GEMS & ESCAPE!', {{ fontSize: '14px', fill: '#93c5fd' }}).setOrigin(0.5);
    }}

    function update() {{
      if (!gameActive) return;
      player.setVelocity(0);
      if (cursors.left.isDown) player.setVelocityX(-220);
      else if (cursors.right.isDown) player.setVelocityX(220);
      if (cursors.up.isDown) player.setVelocityY(-220);
      else if (cursors.down.isDown) player.setVelocityY(220);
    }}

    function collectGem(player, gem) {{
      gem.destroy(); playSound('collect'); score += 1;
      scoreText.setText('Knowledge Gems: ' + score + ' / 5');
    }}

    function reachExit(player, portal) {{
      if (score >= 5) {{
        gameActive = false; playSound('win'); player.setTint(0x4ade80);
        statusText.setText('🎉 MAZE COMPLETED! ALL KNOWLEDGE UNLOCKED!');
      }} else {{
        statusText.setText('⚠️ Collect all 5 Gems before exiting!');
      }}
    }}
  </script>
</body>
</html>"""


# ==============================================================================
# GENRE 3: Space Defender Shooter
# ==============================================================================
def build_space_shooter_game(gdd: Dict[str, Any], palette: Dict[str, Any]) -> str:
    title = gdd.get("game_title", "Space Defender")
    colors = palette.get("colors", {})
    bg_color = colors.get("background", "#0b0f19")
    player_color = colors.get("player", "#38bdf8")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{ margin: 0; padding: 0; background-color: {bg_color}; color: #fff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
    #game-container {{ border: 3px solid #1e293b; border-radius: 12px; overflow: hidden; }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/phaser@3.80.0/dist/phaser.min.js"></script>
</head>
<body>
  <div id="game-container"></div>
  <script>
    function playSound(type) {{
      try {{
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator(); const gain = ctx.createGain();
        osc.connect(gain); gain.connect(ctx.destination); const now = ctx.currentTime;
        if (type === 'shoot') {{
          osc.type = 'sawtooth'; osc.frequency.setValueAtTime(800, now); osc.frequency.exponentialRampToValueAtTime(100, now + 0.15);
          gain.gain.setValueAtTime(0.2, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
          osc.start(now); osc.stop(now + 0.15);
        }} else if (type === 'hit') {{
          osc.type = 'square'; osc.frequency.setValueAtTime(150, now); osc.frequency.exponentialRampToValueAtTime(30, now + 0.25);
          gain.gain.setValueAtTime(0.3, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
          osc.start(now); osc.stop(now + 0.25);
        }} else if (type === 'collect') {{
          osc.type = 'sine'; osc.frequency.setValueAtTime(523.25, now); osc.frequency.setValueAtTime(659.25, now + 0.08);
          gain.gain.setValueAtTime(0.2, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
          osc.start(now); osc.stop(now + 0.2);
        }}
      }} catch(e) {{}}
    }}

    const config = {{
      type: Phaser.AUTO, width: 800, height: 600, parent: 'game-container', backgroundColor: '{bg_color}',
      physics: {{ default: 'arcade', arcade: {{ gravity: {{ y: 0 }}, debug: false }} }},
      scene: {{ preload: preload, create: create, update: update }}
    }};

    let player, lasers, targets, hazards, cursors, fireKey;
    let score = 0, shields = 3, lastFired = 0, gameActive = true;
    let scoreText, shieldText;

    const game = new Phaser.Game(config);

    function preload() {{
      let g = this.add.graphics();
      g.fillStyle(parseInt("{player_color}".replace("#","0x")), 1); g.fillTriangle(20, 0, 0, 40, 40, 40); g.generateTexture('ship_tex', 40, 40); g.clear();
      g.fillStyle(0x38bdf8, 1); g.fillRect(0, 0, 6, 16); g.generateTexture('laser_tex', 6, 16); g.clear();
      g.fillStyle(0x4ade80, 1); g.fillCircle(18, 18, 18); g.generateTexture('target_tex', 36, 36); g.clear();
      g.fillStyle(0xf87171, 1); g.fillRect(0, 0, 32, 32); g.generateTexture('hazard_tex', 32, 32); g.destroy();
    }}

    function create() {{
      player = this.physics.add.sprite(400, 540, 'ship_tex'); player.setCollideWorldBounds(true);
      cursors = this.input.keyboard.createCursorKeys(); fireKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
      lasers = this.physics.add.group({{ defaultKey: 'laser_tex', maxSize: 20 }});
      targets = this.physics.add.group(); hazards = this.physics.add.group();

      scoreText = this.add.text(16, 16, 'Score: 0', {{ fontSize: '22px', fill: '#4ade80', fontWeight: 'bold' }});
      shieldText = this.add.text(660, 16, 'Shields: ❤️❤️❤️', {{ fontSize: '20px', fill: '#f87171' }});

      this.time.addEvent({{ delay: 1300, callback: spawnWave, callbackScope: this, loop: true }});
      this.physics.add.overlap(lasers, targets, destroyTarget, null, this);
      this.physics.add.overlap(lasers, hazards, destroyHazard, null, this);
      this.physics.add.overlap(player, hazards, hitPlayer, null, this);
    }}

    function update(time) {{
      if (!gameActive) return;
      if (cursors.left.isDown) player.setVelocityX(-400);
      else if (cursors.right.isDown) player.setVelocityX(400);
      else player.setVelocityX(0);

      if (fireKey.isDown && time > lastFired) {{
        let laser = lasers.get(player.x, player.y - 20);
        if (laser) {{
          playSound('shoot');
          laser.setActive(true).setVisible(true); laser.body.velocity.y = -600;
          lastFired = time + 180;
        }}
      }}
    }}

    function spawnWave() {{
      if (!gameActive) return;
      let x = Phaser.Math.Between(50, 750);
      if (Math.random() > 0.4) {{
        let t = targets.create(x, -20, 'target_tex'); t.setVelocityY(140);
      }} else {{
        let h = hazards.create(x, -20, 'hazard_tex'); h.setVelocityY(180);
      }}
    }}

    function destroyTarget(laser, target) {{
      playSound('collect'); laser.setActive(false).setVisible(false); target.destroy();
      score += 250; scoreText.setText('Score: ' + score);
    }}

    function destroyHazard(laser, hazard) {{
      playSound('hit'); laser.setActive(false).setVisible(false); hazard.destroy();
      score += 50; scoreText.setText('Score: ' + score);
    }}

    function hitPlayer(player, hazard) {{
      playSound('hit'); hazard.destroy(); shields--;
      if (shields <= 0) {{
        shieldText.setText('Shields: ❌'); gameActive = false; player.setTint(0xff0000);
        this.add.text(400, 300, 'GAME OVER\\nRefresh to Retry', {{ fontSize: '34px', fill: '#ff4757', align: 'center' }}).setOrigin(0.5);
      }} else {{
        shieldText.setText('Shields: ' + '❤️'.repeat(shields));
      }}
    }}
  </script>
</body>
</html>"""


# ==============================================================================
# GENRE 4: Gravity Runner
# ==============================================================================
def build_gravity_runner_game(gdd: Dict[str, Any], palette: Dict[str, Any]) -> str:
    title = gdd.get("game_title", "Gravity Runner")
    colors = palette.get("colors", {})
    bg_color = colors.get("background", "#0a0a16")
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{ margin: 0; padding: 0; background-color: {bg_color}; color: #fff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
    #game-container {{ border: 3px solid #38bdf8; border-radius: 12px; overflow: hidden; }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/phaser@3.80.0/dist/phaser.min.js"></script>
</head>
<body>
  <div id="game-container"></div>
  <script>
    function playSound(type) {{
      try {{
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator(); const gain = ctx.createGain();
        osc.connect(gain); gain.connect(ctx.destination); const now = ctx.currentTime;
        if (type === 'collect') {{
          osc.type = 'sine'; osc.frequency.setValueAtTime(523.25, now); osc.frequency.setValueAtTime(659.25, now + 0.08);
          gain.gain.setValueAtTime(0.2, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
          osc.start(now); osc.stop(now + 0.2);
        }} else if (type === 'hit') {{
          osc.type = 'square'; osc.frequency.setValueAtTime(150, now); osc.frequency.exponentialRampToValueAtTime(30, now + 0.25);
          gain.gain.setValueAtTime(0.3, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
          osc.start(now); osc.stop(now + 0.25);
        }}
      }} catch(e) {{}}
    }}

    const config = {{
      type: Phaser.AUTO, width: 800, height: 600, parent: 'game-container', backgroundColor: '{bg_color}',
      physics: {{ default: 'arcade', arcade: {{ gravity: {{ y: 900 }}, debug: false }} }},
      scene: {{ preload: preload, create: create, update: update }}
    }};

    let player, floor, ceiling, obstacles, energyOrbs, spaceKey;
    let gravityFlipped = false, score = 0, gameActive = true, scoreText;

    const game = new Phaser.Game(config);

    function preload() {{
      let g = this.add.graphics();
      g.fillStyle(0xc084fc, 1); g.fillRect(0, 0, 32, 32); g.generateTexture('runner_tex', 32, 32); g.clear();
      g.fillStyle(0x4ade80, 1); g.fillCircle(14, 14, 14); g.generateTexture('orb_tex', 28, 28); g.clear();
      g.fillStyle(0xf87171, 1); g.fillTriangle(16, 0, 0, 32, 32, 32); g.generateTexture('spike_tex', 32, 32); g.destroy();
    }}

    function create() {{
      floor = this.physics.add.staticGroup(); ceiling = this.physics.add.staticGroup();
      let g = this.add.graphics(); g.fillStyle(0x1e293b, 1); g.fillRect(0, 0, 800, 20); g.generateTexture('platform_tex', 800, 20); g.destroy();

      floor.create(400, 590, 'platform_tex'); ceiling.create(400, 10, 'platform_tex');
      player = this.physics.add.sprite(150, 530, 'runner_tex'); player.setCollideWorldBounds(true);
      this.physics.add.collider(player, floor); this.physics.add.collider(player, ceiling);

      spaceKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
      obstacles = this.physics.add.group(); energyOrbs = this.physics.add.group();

      scoreText = this.add.text(16, 30, 'Distance / Energy: 0', {{ fontSize: '20px', fill: '#38bdf8', fontWeight: 'bold' }});
      this.time.addEvent({{ delay: 1400, callback: spawnObstacles, callbackScope: this, loop: true }});

      this.physics.add.overlap(player, energyOrbs, collectOrb, null, this);
      this.physics.add.overlap(player, obstacles, hitSpike, null, this);
    }}

    function update() {{
      if (!gameActive) return;
      if (Phaser.Input.Keyboard.JustDown(spaceKey)) {{
        playSound('collect');
        gravityFlipped = !gravityFlipped;
        this.physics.world.gravity.y = gravityFlipped ? -900 : 900;
        player.setFlipY(gravityFlipped);
      }}
      score += 1; scoreText.setText('Distance / Energy: ' + score);
    }}

    function spawnObstacles() {{
      if (!gameActive) return;
      let isTop = Math.random() > 0.5;
      if (Math.random() > 0.3) {{
        let orb = energyOrbs.create(820, isTop ? 70 : 530, 'orb_tex'); orb.body.allowGravity = false; orb.setVelocityX(-320);
      }} else {{
        let spike = obstacles.create(820, isTop ? 40 : 560, 'spike_tex'); spike.body.allowGravity = false; spike.setVelocityX(-320);
        if (isTop) spike.setFlipY(true);
      }}
    }}

    function collectOrb(player, orb) {{ orb.destroy(); playSound('collect'); score += 200; }}
    function hitSpike(player, spike) {{
      playSound('hit'); gameActive = false; this.physics.pause(); player.setTint(0xff0000);
      this.add.text(400, 300, 'GRAVITY RUNNER CRASHED!\\nRefresh to Retry', {{ fontSize: '32px', fill: '#f87171', align: 'center' }}).setOrigin(0.5);
    }}
  </script>
</body>
</html>"""


# ==============================================================================
# GENRE 5: Slingshot Launcher
# ==============================================================================
def build_slingshot_launcher_game(gdd: Dict[str, Any], palette: Dict[str, Any]) -> str:
    title = gdd.get("game_title", "Slingshot Physics")
    colors = palette.get("colors", {})
    bg_color = colors.get("background", "#0f172a")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{ margin: 0; padding: 0; background-color: {bg_color}; color: #fff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
    #game-container {{ border: 3px solid #4ade80; border-radius: 12px; overflow: hidden; }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/phaser@3.80.0/dist/phaser.min.js"></script>
</head>
<body>
  <div id="game-container"></div>
  <script>
    function playSound(type) {{
      try {{
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator(); const gain = ctx.createGain();
        osc.connect(gain); gain.connect(ctx.destination); const now = ctx.currentTime;
        if (type === 'shoot') {{
          osc.type = 'sawtooth'; osc.frequency.setValueAtTime(600, now); osc.frequency.exponentialRampToValueAtTime(150, now + 0.15);
          gain.gain.setValueAtTime(0.2, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
          osc.start(now); osc.stop(now + 0.15);
        }} else if (type === 'collect') {{
          osc.type = 'sine'; osc.frequency.setValueAtTime(523.25, now); osc.frequency.setValueAtTime(659.25, now + 0.08);
          gain.gain.setValueAtTime(0.2, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
          osc.start(now); osc.stop(now + 0.2);
        }}
      }} catch(e) {{}}
    }}

    const config = {{
      type: Phaser.AUTO, width: 800, height: 600, parent: 'game-container', backgroundColor: '{bg_color}',
      physics: {{ default: 'arcade', arcade: {{ gravity: {{ y: 400 }}, debug: false }} }},
      scene: {{ preload: preload, create: create, update: update }}
    }};

    let projectile, targets, isDragging = false, launchPos = {{ x: 150, y: 450 }}, line, score = 0, scoreText;

    const game = new Phaser.Game(config);

    function preload() {{
      let g = this.add.graphics();
      g.fillStyle(0x38bdf8, 1); g.fillCircle(16, 16, 16); g.generateTexture('ball_tex', 32, 32); g.clear();
      g.fillStyle(0x4ade80, 1); g.fillRect(0, 0, 40, 40); g.generateTexture('block_tex', 40, 40); g.destroy();
    }}

    function create() {{
      line = this.add.graphics();
      projectile = this.physics.add.sprite(launchPos.x, launchPos.y, 'ball_tex');
      projectile.setCollideWorldBounds(true); projectile.body.allowGravity = false;

      targets = this.physics.add.group();
      for(let i=0; i<5; i++) {{
        for(let j=0; j<3; j++) {{
          let b = targets.create(550 + j*45, 200 + i*45, 'block_tex');
          b.body.allowGravity = false; b.setImmovable(true);
        }}
      }}

      scoreText = this.add.text(16, 16, 'Score: 0', {{ fontSize: '22px', fill: '#4ade80', fontWeight: 'bold' }});
      this.input.on('pointerdown', startDrag, this);
      this.input.on('pointermove', doDrag, this);
      this.input.on('pointerup', releaseLaunch, this);

      this.physics.add.collider(projectile, targets, hitBlock, null, this);
    }}

    function update() {{}}
    function startDrag(pointer) {{ if (Phaser.Math.Distance.Between(pointer.x, pointer.y, projectile.x, projectile.y) < 50) isDragging = true; }}
    function doDrag(pointer) {{
      if (isDragging) {{
        projectile.x = pointer.x; projectile.y = pointer.y;
        line.clear(); line.lineStyle(3, 0xfbbf24, 1); line.lineBetween(launchPos.x, launchPos.y, pointer.x, pointer.y);
      }}
    }}
    function releaseLaunch(pointer) {{
      if (isDragging) {{
        isDragging = false; line.clear(); playSound('shoot');
        let dx = launchPos.x - projectile.x; let dy = launchPos.y - projectile.y;
        projectile.body.allowGravity = true; projectile.setVelocity(dx * 4, dy * 4);
      }}
    }}
    function hitBlock(proj, block) {{ block.destroy(); playSound('collect'); score += 200; scoreText.setText('Score: ' + score); }}
  </script>
</body>
</html>"""


# ==============================================================================
# GENRE 6: Vehicle Slalom Dodger
# ==============================================================================
def build_vehicle_slalom_game(gdd: Dict[str, Any], palette: Dict[str, Any]) -> str:
    title = gdd.get("game_title", "Cyber Slalom")
    colors = palette.get("colors", {})
    bg_color = colors.get("background", "#0d1117")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{ margin: 0; padding: 0; background-color: {bg_color}; color: #fff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
    #game-container {{ border: 3px solid #c084fc; border-radius: 12px; overflow: hidden; }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/phaser@3.80.0/dist/phaser.min.js"></script>
</head>
<body>
  <div id="game-container"></div>
  <script>
    function playSound(type) {{
      try {{
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator(); const gain = ctx.createGain();
        osc.connect(gain); gain.connect(ctx.destination); const now = ctx.currentTime;
        if (type === 'collect') {{
          osc.type = 'sine'; osc.frequency.setValueAtTime(523.25, now); osc.frequency.setValueAtTime(659.25, now + 0.08);
          gain.gain.setValueAtTime(0.2, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
          osc.start(now); osc.stop(now + 0.2);
        }} else if (type === 'hit') {{
          osc.type = 'square'; osc.frequency.setValueAtTime(150, now); osc.frequency.exponentialRampToValueAtTime(30, now + 0.25);
          gain.gain.setValueAtTime(0.3, now); gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
          osc.start(now); osc.stop(now + 0.25);
        }}
      }} catch(e) {{}}
    }}

    const config = {{
      type: Phaser.AUTO, width: 800, height: 600, parent: 'game-container', backgroundColor: '{bg_color}',
      physics: {{ default: 'arcade', arcade: {{ gravity: {{ y: 0 }}, debug: false }} }},
      scene: {{ preload: preload, create: create, update: update }}
    }};

    let car, boostPads, hazards, cursors, lanes = [220, 400, 580], currentLane = 1, score = 0, scoreText, gameActive = true;

    const game = new Phaser.Game(config);

    function preload() {{
      let g = this.add.graphics();
      g.fillStyle(0xc084fc, 1); g.fillTriangle(20, 0, 0, 50, 40, 50); g.generateTexture('car_tex', 40, 50); g.clear();
      g.fillStyle(0x38bdf8, 1); g.fillRect(0, 0, 50, 20); g.generateTexture('boost_tex', 50, 20); g.clear();
      g.fillStyle(0xf87171, 1); g.fillCircle(20, 20, 20); g.generateTexture('oil_tex', 40, 40); g.destroy();
    }}

    function create() {{
      let g = this.add.graphics(); g.lineStyle(4, 0x334155, 1); g.lineBetween(310, 0, 310, 600); g.lineBetween(490, 0, 490, 600);
      car = this.physics.add.sprite(lanes[currentLane], 500, 'car_tex');
      cursors = this.input.keyboard.createCursorKeys();
      boostPads = this.physics.add.group(); hazards = this.physics.add.group();

      scoreText = this.add.text(16, 16, 'Speed Score: 0', {{ fontSize: '22px', fill: '#38bdf8', fontWeight: 'bold' }});
      this.time.addEvent({{ delay: 1000, callback: spawnRoadItems, callbackScope: this, loop: true }});

      this.physics.add.overlap(car, boostPads, hitBoost, null, this);
      this.physics.add.overlap(car, hazards, hitOil, null, this);
    }}

    function update() {{
      if (!gameActive) return;
      if (Phaser.Input.Keyboard.JustDown(cursors.left) && currentLane > 0) {{ currentLane--; car.x = lanes[currentLane]; }}
      else if (Phaser.Input.Keyboard.JustDown(cursors.right) && currentLane < 2) {{ currentLane++; car.x = lanes[currentLane]; }}
    }}

    function spawnRoadItems() {{
      if (!gameActive) return;
      let laneIdx = Phaser.Math.Between(0, 2);
      if (Math.random() > 0.4) {{
        let b = boostPads.create(lanes[laneIdx], -30, 'boost_tex'); b.setVelocityY(350);
      }} else {{
        let h = hazards.create(lanes[laneIdx], -30, 'oil_tex'); h.setVelocityY(350);
      }}
    }}

    function hitBoost(car, boost) {{ boost.destroy(); playSound('collect'); score += 300; scoreText.setText('Speed Score: ' + score); }}
    function hitOil(car, oil) {{
      oil.destroy(); playSound('hit'); score = Math.max(0, score - 150); scoreText.setText('Speed Score: ' + score);
    }}
  </script>
</body>
</html>"""
