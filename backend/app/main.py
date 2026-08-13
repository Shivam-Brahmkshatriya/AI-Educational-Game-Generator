import os
import json
import asyncio
import logging
from typing import Dict, Any, Optional
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.config import OUTPUT_DIR, PORT, HOST
from app.graph.workflow import create_game_generator_graph
from langgraph.types import Command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

app = FastAPI(title="Local Ollama AI Educational Game Generator", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount generated games as static files
app.mount("/games", StaticFiles(directory=str(OUTPUT_DIR)), name="games")

# Global graph instance
graph_app = create_game_generator_graph()

# In-memory session tracker
active_sessions: Dict[str, Dict[str, Any]] = {}

class GenerateRequest(BaseModel):
    topic: str
    genre_override: Optional[str] = None
    target_grade: Optional[str] = "Middle School (6-8)"

class HitlResumeRequest(BaseModel):
    session_id: str
    action: str  # "approved" or "rejected"
    feedback: str = ""

@app.get("/api/health")
def health_check():
    return {"status": "ok", "model": "ollama/gemma4:latest"}

@app.post("/api/generate")
async def start_generation(req: GenerateRequest):
    topic = req.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
    session_id = f"sess_{int(asyncio.get_event_loop().time() * 1000)}"
    active_sessions[session_id] = {
        "session_id": session_id,
        "topic": topic,
        "genre_override": req.genre_override,
        "target_grade": req.target_grade,
        "status": "initialized",
        "logs": [],
        "gdd": None,
        "hitl_pending": False,
        "output_url": None
    }
    
    logger.info(f"Initialized session '{session_id}' | Topic: '{topic}' | Genre Override: '{req.genre_override}' | Grade: '{req.target_grade}'")
    return {"session_id": session_id, "topic": topic, "genre_override": req.genre_override, "target_grade": req.target_grade}

@app.post("/api/hitl/resume")
async def resume_hitl(req: HitlResumeRequest):
    session_id = req.session_id
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
        
    session = active_sessions[session_id]
    session["hitl_pending"] = False
    
    config = {"configurable": {"thread_id": session_id}}
    command = Command(resume={"action": req.action, "feedback": req.feedback})
    
    asyncio.create_task(run_graph_execution(session_id, command_resume=command))
    return {"status": "resumed", "session_id": session_id, "action": req.action}

@app.get("/api/games")
def list_generated_games():
    games = []
    if OUTPUT_DIR.exists():
        for d in OUTPUT_DIR.iterdir():
            if d.is_dir() and (d / "index.html").exists():
                games.append({
                    "title": d.name.replace("_", " ").title(),
                    "folder": d.name,
                    "url": f"/games/{d.name}/index.html"
                })
    return games

async def run_graph_execution(session_id: str, input_state: Dict[str, Any] = None, command_resume: Any = None):
    config = {"configurable": {"thread_id": session_id}}
    session = active_sessions.get(session_id)
    if not session:
        return

    try:
        if command_resume:
            stream = graph_app.astream(command_resume, config, stream_mode="values")
        else:
            stream = graph_app.astream(input_state, config, stream_mode="values")

        async for event in stream:
            session["logs"] = event.get("logs", [])
            session["gdd"] = event.get("gdd", None)
            
            out_path = event.get("output_path")
            if out_path:
                rel_path = Path(out_path).parent.name
                session["output_url"] = f"/games/{rel_path}/index.html"
                
            ws = session.get("ws")
            if ws:
                await ws.send_json({
                    "type": "state_update",
                    "session_id": session_id,
                    "gdd": event.get("gdd"),
                    "logs": event.get("logs", []),
                    "output_url": session.get("output_url"),
                    "hitl_status": event.get("hitl_status"),
                    "qa_passed": event.get("qa_passed")
                })
                
        state_info = graph_app.get_state(config)
        if state_info.next and "hitl_breakpoint" in state_info.next:
            session["hitl_pending"] = True
            session["status"] = "hitl_pending"
            ws = session.get("ws")
            if ws:
                await ws.send_json({
                    "type": "hitl_required",
                    "session_id": session_id,
                    "gdd": session.get("gdd")
                })
        else:
            session["status"] = "completed"
            ws = session.get("ws")
            if ws:
                await ws.send_json({
                    "type": "generation_completed",
                    "session_id": session_id,
                    "output_url": session.get("output_url")
                })
    except Exception as e:
        logger.error(f"Execution graph error for session {session_id}: {e}")
        session["status"] = "failed"
        ws = session.get("ws")
        if ws:
            await ws.send_json({"type": "error", "message": str(e)})

@app.websocket("/ws/pipeline/{session_id}")
async def websocket_pipeline(websocket: WebSocket, session_id: str):
    await websocket.accept()
    if session_id not in active_sessions:
        await websocket.send_json({"type": "error", "message": "Session not found"})
        await websocket.close()
        return

    session = active_sessions[session_id]
    session["ws"] = websocket
    
    if session["status"] == "initialized":
        session["status"] = "running"
        initial_input = {
            "topic": session["topic"],
            "genre_override": session.get("genre_override"),
            "target_grade": session.get("target_grade")
        }
        asyncio.create_task(run_graph_execution(session_id, input_state=initial_input))

    try:
        while True:
            await websocket.receive_text()
            await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        session["ws"] = None
        logger.info(f"WebSocket client disconnected from session {session_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
