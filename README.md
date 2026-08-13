# 🎮 AI Educational Game Generator (v2.0)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Python-FF6F61.svg?style=flat)](https://github.com/langchain-ai/langgraph)
[![Phaser3](https://img.shields.io/badge/Phaser-3.80+-E65100.svg?style=flat&logo=phaser&logoColor=white)](https://phaser.io/)
[![Vite](https://img.shields.io/badge/Vite-6.0+-646CFF.svg?style=flat&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-000000.svg?style=flat)](https://ollama.ai/)
[![Playwright](https://img.shields.io/badge/Playwright-Automated_QA-45BA4B.svg?style=flat&logo=playwright&logoColor=white)](https://playwright.dev/)

An autonomous, multi-agent AI system that generates playable, novel HTML5 educational games based on user-provided topics. Powered by local LLMs via **Ollama**, orchestrated with **LangGraph**, verified using **Playwright**, and rendered with **Phaser 3**, **WebAudio API sound synthesis**, and custom interactive HTML5 canvas components.

---

## 🚀 Version Evolution: v1.0 ➔ v2.0

### 📌 Version 1.0 (Baseline Architecture)
* **Autonomous Multi-Agent Pipeline**: LangGraph orchestration powered by local Ollama LLMs (`gemma4:latest`).
* **Compound Researcher**: Web searching via `DDGS` / Bing to harvest educational facts.
* **Human-In-The-Loop (HITL) Gate**: Interactive GDD approval breakpoint prior to code synthesis.
* **Automated Browser QA**: Playwright Chromium testing to capture runtime console errors before delivery.

### 🌟 Version 2.0 (Advanced Audio-Visual & Engine Upgrade)
* 🔊 **Procedural WebAudio SFX Engine**: Synthesizes retro sound effects (laser pulses, collisions, engine revs, power-up pickups, victory chimes) directly in the browser with zero external MP3/WAV file dependencies.
* 🎮 **13 Universal Gameplay Genre Engines**: Comprehensive support for 13 distinct 2D game mechanics (Brick Breakers, Side-Scrolling Platformers, Bubble Shooters, Tower Defense, Top-Down RPG Quests, Memory Cards, Word Solvers, Maze Explorers, Slingshot Physics, Gravity Runners, Vehicle Slalom, Space Defense, and Grid/Board Games).
* 🎛️ **Genre & Grade Level Configuration Controls**: Allows users to manually force specific gameplay genres or configure target grade difficulty (Elementary K-5, Middle School 6-8, High School AP, College/Adult) from the dashboard UI.
* 📊 **Post-Game Mastery Analytics Report**: Displays an interactive student performance report after gameplay, tracking accuracy rating, concept attempts, and awarding achievement badges (e.g. *Master Strategist*, *Concept Apprentice*).
* 💾 **1-Click Standalone HTML Export**: Download self-contained HTML files containing full Phaser engine code, WebAudio synthesizers, and embedded styles for offline LMS deployment.

---

## 🏗️ Architecture & Multi-Agent Pipeline

The generation pipeline is built using **LangGraph** stateful workflows:

```mermaid
flowchart TD
    A[User Topic & Manual Controls] --> B[Researcher Agent]
    B --> C[Design Directorate]
    
    subgraph Design Directorate [Design Directorate]
        C1[Mechanics Agent]
        C2[Narrative Designer]
        C3[Pedagogy Agent]
    end

    C1 --> D[Master Designer Agent]
    C2 --> D
    C3 --> D

    D --> E[Critic Agent]
    E -- Rejected --> D
    E -- Approved --> F{HITL Approval Gate}
    
    F -- User Rejection / Feedback --> D
    F -- User Approved --> G[Asset Artist Agent]
    
    G --> H[Lead Developer Agent + WebAudio SFX]
    H --> I[Playwright QA Tester]
    
    I -- Failed Code / Runtime Error --> H
    I -- Passed Automated Browser QA --> J[Playable Game Asset + Analytics]
```

---

## 🎲 Supported v2.0 Gameplay Genres

1. 🧱 **Brick Breaker / Arkanoid Paddle Physics**: Control a horizontal paddle to bounce balls, smash concept bricks, and trigger power-ups.
2. 🏃 **2D Side-Scrolling Jump & Run Platformer**: Classic Mario/Sonic style platformer with pit jumping, enemy stomping, and finish flags.
3. 🔮 **Bubble Shooter / Match-3 Cannon**: Aim and fire colored concept spheres at matching clusters to trigger chain reactions.
4. 🏰 **Tower Defense & Base Guardian**: Place strategic defensive turrets along a path to destroy incoming wave creeps.
5. 🧙‍♂️ **Top-Down Retro RPG Quest & Battle**: Explore an 8-bit overworld map, talk to wizard NPCs, and battle boss encounters.
6. 🎴 **Card Match & Memory Concentration**: Flip hidden cards to pair matching educational terms, formulas, and visual diagrams.
7. 🔤 **Word Scramble & Vocabulary Solver**: Unscramble missing educational terms and formula keywords letter-by-letter.
8. ⭕ **Grid / Board / Turn-Based Game**: 3x3 or 4x4 strategic board games (Tic-Tac-Toe, Matrix Match, Grid Puzzle).
9. 🗺️ **Maze & Dungeon Explorer**: Navigate tile grid dungeons, collect knowledge gems, and reach exit portals.
10. 🎯 **Physics Slingshot & Trajectory Launcher**: Drag and launch projectiles with angle/velocity vectors to smash target towers.
11. 🤸 **Gravity-Flipping Runner Platformer**: Invert gravity between floor and ceiling while running automatically at high speed.
12. 🏎️ **High-Speed Slalom / Vehicle Dodger**: Drive a futuristic hover-car through 3 highway lanes to collect speed-boosting facts.
13. 🚀 **Arcade Space & Defense Shooter**: Pilot a starship to blast laser pulses at incoming asteroid hazards and target nodes.

---

## 🛠️ Technology Stack

* **Backend**: Python 3.10+, FastAPI, LangGraph, SQLite, Uvicorn, WebSockets
* **Local LLM**: Ollama (`gemma4:latest` or `llama3`)
* **Automated QA**: Playwright (Headless Chromium)
* **Frontend**: React 19, Vite 8, Lucide Icons, Canvas Confetti
* **Game Engines**: Phaser 3 (CDN), WebAudio API, HTML5 Canvas, Vanilla JS / CSS

---

## 🏃 Running the Application

### 1. Start Backend Server (FastAPI on Port 8000)
```bash
source venv/bin/activate
PYTHONPATH=backend uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Start Frontend App (React / Vite on Port 5173)
```bash
cd frontend
npm run dev -- --host 0.0.0.0 --port 5173
```

Open **`http://localhost:5173/`** in your browser!
