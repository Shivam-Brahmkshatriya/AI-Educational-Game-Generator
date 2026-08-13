import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Literal
import sqlite3

from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt

from app.config import SQLITE_DB_PATH, OUTPUT_DIR
from app.graph.state import GameState

from app.agents.researcher import run_researcher
from app.agents.mechanics import run_mechanic_agent
from app.agents.narrative import run_narrative_agent
from app.agents.educational import run_educational_agent
from app.agents.master_designer import run_master_designer
from app.agents.critic import run_critic_agent
from app.agents.asset_artist import run_asset_artist
from app.agents.lead_developer import run_lead_developer
from app.agents.qa_tester import run_qa_tester
from app.qa.runner import run_playwright_qa_test

logger = logging.getLogger(__name__)

# --- AGENT NODES ---

async def researcher_node(state: GameState) -> Dict[str, Any]:
    topic = state.get("topic", "Fractions")
    facts = await run_researcher(topic)
    return {
        "research_facts": facts,
        "logs": state.get("logs", []) + [{"agent": "Researcher", "status": "completed", "message": f"Extracted {len(facts)} facts about '{topic}'."}]
    }

async def design_subagents_node(state: GameState) -> Dict[str, Any]:
    topic = state["topic"]
    facts = state["research_facts"]
    
    # Run sub-agents in parallel
    mechanics_task = run_mechanic_agent(topic, facts, genre_override=state.get("genre_override"))
    narrative_task = run_narrative_agent(topic)
    edu_task = run_educational_agent(topic, facts)
    
    mechanics, narrative, edu = await asyncio.gather(mechanics_task, narrative_task, edu_task)
    
    return {
        "mechanics_idea": mechanics,
        "narrative_idea": narrative,
        "educational_idea": edu,
        "logs": state.get("logs", []) + [{"agent": "Design Directorate", "status": "completed", "message": "Specialist sub-agents compiled domain concepts."}]
    }

async def master_designer_node(state: GameState) -> Dict[str, Any]:
    feedback = state.get("user_feedback", "") or state.get("critic_feedback", "")
    gdd = await run_master_designer(
        topic=state["topic"],
        research_facts=state["research_facts"],
        mechanics_idea=state.get("mechanics_idea", ""),
        narrative_idea=state.get("narrative_idea", ""),
        educational_idea=state.get("educational_idea", ""),
        feedback=feedback
    )
    return {
        "gdd": gdd,
        "user_feedback": "", # reset after incorporation
        "logs": state.get("logs", []) + [{"agent": "Master Designer", "status": "completed", "message": f"Compiled canonical GDD: '{gdd.get('game_title')}'."}]
    }

async def critic_node(state: GameState) -> Dict[str, Any]:
    approved, feedback = await run_critic_agent(state["gdd"])
    return {
        "critic_approved": approved,
        "critic_feedback": feedback,
        "logs": state.get("logs", []) + [{"agent": "Critic", "status": "completed", "message": f"Review result: Approved={approved}."}]
    }

async def hitl_breakpoint_node(state: GameState) -> Dict[str, Any]:
    """
    Pause execution and wait for Human In The Loop review approval/rejection.
    """
    # Trigger LangGraph interrupt for human intervention
    logger.info("HITL Breakpoint triggered: Pausing graph execution for user GDD approval...")
    
    human_decision = interrupt({
        "message": "Human Review Required: Inspect GDD and Approve/Reject",
        "gdd": state["gdd"]
    })
    
    # After resume, human_decision contains {"action": "approve" / "reject", "feedback": "..."}
    status = human_decision.get("action", "approved")
    feedback = human_decision.get("feedback", "")
    
    return {
        "hitl_status": status,
        "user_feedback": feedback,
        "logs": state.get("logs", []) + [{"agent": "HITL Gate", "status": "resume", "message": f"User action: {status}. Feedback: '{feedback}'"}]
    }

async def asset_artist_node(state: GameState) -> Dict[str, Any]:
    palette = await run_asset_artist(state["gdd"])
    return {
        "asset_palette": palette,
        "logs": state.get("logs", []) + [{"agent": "Asset Artist", "status": "completed", "message": "Generated procedural graphics specifications."}]
    }

async def lead_developer_node(state: GameState) -> Dict[str, Any]:
    code = await run_lead_developer(
        gdd=state["gdd"],
        asset_palette=state["asset_palette"],
        qa_report=state.get("qa_report", {})
    )
    
    # Save code to output directory
    game_title = state["gdd"].get("game_title", "game").lower().replace(" ", "_")
    game_dir = OUTPUT_DIR / game_title
    game_dir.mkdir(parents=True, exist_ok=True)
    out_file = game_dir / "index.html"
    out_file.write_text(code, encoding="utf-8")
    
    return {
        "generated_code": code,
        "output_path": str(out_file),
        "qa_iterations": state.get("qa_iterations", 0) + 1,
        "logs": state.get("logs", []) + [{"agent": "Lead Developer", "status": "completed", "message": f"Authored Phaser 3 game code ({len(code)} bytes) -> {out_file.name}"}]
    }

async def qa_tester_node(state: GameState) -> Dict[str, Any]:
    out_path = Path(state["output_path"])
    playwright_res = await run_playwright_qa_test(out_path)
    qa_report = await run_qa_tester(playwright_res)
    
    return {
        "qa_passed": qa_report.get("passed", False),
        "qa_report": qa_report,
        "logs": state.get("logs", []) + [{"agent": "QA Tester", "status": "completed", "message": f"Playwright QA Result: Passed={qa_report.get('passed')}."}]
    }

# --- CONDITIONAL ROUTING ---

def route_after_critic(state: GameState) -> str:
    if state.get("critic_approved"):
        return "hitl_breakpoint"
    else:
        return "master_designer"

def route_after_hitl(state: GameState) -> str:
    if state.get("hitl_status") == "rejected":
        return "master_designer"
    return "asset_artist"

def route_after_qa(state: GameState) -> str:
    if state.get("qa_passed"):
        return END
    if state.get("qa_iterations", 0) >= 3:
        logger.warning("Reached max QA iterations (3). Delivering game.")
        return END
    return "lead_developer"

# --- GRAPH CONSTRUCTION ---

def create_game_generator_graph():
    builder = StateGraph(GameState)
    
    # Add Nodes
    builder.add_node("researcher", researcher_node)
    builder.add_node("design_subagents", design_subagents_node)
    builder.add_node("master_designer", master_designer_node)
    builder.add_node("critic", critic_node)
    builder.add_node("hitl_breakpoint", hitl_breakpoint_node)
    builder.add_node("asset_artist", asset_artist_node)
    builder.add_node("lead_developer", lead_developer_node)
    builder.add_node("qa_tester", qa_tester_node)
    
    # Add Edges
    builder.add_edge(START, "researcher")
    builder.add_edge("researcher", "design_subagents")
    builder.add_edge("design_subagents", "master_designer")
    builder.add_edge("master_designer", "critic")
    
    builder.add_conditional_edges(
        "critic",
        route_after_critic,
        {
            "hitl_breakpoint": "hitl_breakpoint",
            "master_designer": "master_designer"
        }
    )
    
    builder.add_conditional_edges(
        "hitl_breakpoint",
        route_after_hitl,
        {
            "master_designer": "master_designer",
            "asset_artist": "asset_artist"
        }
    )
    
    builder.add_edge("asset_artist", "lead_developer")
    builder.add_edge("lead_developer", "qa_tester")
    
    builder.add_conditional_edges(
        "qa_tester",
        route_after_qa,
        {
            "lead_developer": "lead_developer",
            END: END
        }
    )
    
    # Setup Checkpointer for HITL state pause/resume
    checkpointer = MemorySaver()
    
    return builder.compile(checkpointer=checkpointer)
