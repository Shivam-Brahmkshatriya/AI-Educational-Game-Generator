import asyncio
import json
import logging
from app.graph.workflow import create_game_generator_graph

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

async def test_bike_game_generation():
    graph = create_game_generator_graph()
    
    topic = "Motorcycle Highway Dynamics & Friction"
    genre_override = "2D Bike Rider / Motorbike Highway Dodge"
    session_id = "sess_bike_ride_99"
    
    print("\n" + "="*57)
    print(f" TESTING BIKE RIDE GAME GENERATION FOR TOPIC: '{topic}'")
    print("="*57)
    print(f"Session ID: {session_id}\n")
    
    initial_state = {
        "session_id": session_id,
        "topic": topic,
        "genre_override": genre_override,
        "target_grade": "Middle School (6-8)",
        "status": "starting",
        "logs": [],
        "research_facts": [],
        "gdd": {},
        "asset_palette": {},
        "hitl_pending": False,
        "user_approved": False,
        "hitl_feedback": "",
        "generated_code": "",
        "qa_report": {},
        "output_url": "",
        "error": None
    }
    
    config = {"configurable": {"thread_id": session_id}}
    
    # Step 1: Run graph until HITL breakpoint
    async for event in graph.astream(initial_state, config=config):
        for node_name, state_update in event.items():
            if "logs" in state_update and state_update["logs"]:
                latest_log = state_update["logs"][-1]
                print(f"  [Log] {latest_log.get('agent')}: {latest_log.get('message')}")
    
    # Check graph state
    current_state = await graph.aget_state(config)
    
    if current_state.next and "hitl_breakpoint" in current_state.next:
        gdd = current_state.values.get("gdd", {})
        print("\n>>> HITL BREAKPOINT TRIGGERED <<<")
        print(f"  Title: '{gdd.get('game_title')}'")
        print(f"  Genre: '{gdd.get('genre')}'")
        print(f"  Controls: '{gdd.get('player_controls')}'")
        
        print("\n  Submitting HITL Approval...")
        await graph.ainvoke(
            {"user_approved": True, "hitl_pending": False, "hitl_feedback": ""},
            config=config
        )
        
        # Resume graph execution post-HITL
        async for event in graph.astream(None, config=config):
            for node_name, state_update in event.items():
                if "logs" in state_update and state_update["logs"]:
                    latest_log = state_update["logs"][-1]
                    print(f"  [Log] {latest_log.get('agent')}: {latest_log.get('message')}")
        
        final_state = await graph.aget_state(config)
        output_url = final_state.values.get("output_url", "")
        print(f"\n>>> PRODUCTION COMPLETED <<<")
        print(f"  Output URL: {output_url}\n")
    else:
        print("\nGraph completed without hitting HITL breakpoint.")

if __name__ == "__main__":
    asyncio.run(test_bike_game_generation())
