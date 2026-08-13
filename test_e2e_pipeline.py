import asyncio
import json
import httpx
import websockets

async def test_topic(topic: str):
    base_url = "http://localhost:8000"
    print(f"\n=======================================================")
    print(f" TESTING GAME GENERATION FOR TOPIC: '{topic}'")
    print(f"=======================================================")
    
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{base_url}/api/generate", json={"topic": topic})
        data = res.json()
        session_id = data["session_id"]
        print(f"Session ID: {session_id}")

        ws_url = f"ws://localhost:8000/ws/pipeline/{session_id}"
        async with websockets.connect(ws_url) as ws:
            hitl_reached = False
            completed = False
            
            while not (hitl_reached or completed):
                msg_raw = await ws.recv()
                msg = json.loads(msg_raw)
                msg_type = msg.get("type")
                
                if msg_type == "state_update":
                    logs = msg.get("logs", [])
                    if logs:
                        latest = logs[-1]
                        print(f"  [Log] [{latest.get('agent')}] {latest.get('message')}")
                elif msg_type == "hitl_required":
                    print("\n>>> HITL BREAKPOINT TRIGGERED <<<")
                    gdd = msg.get("gdd", {})
                    print(f"  Title: '{gdd.get('game_title')}'")
                    print(f"  Genre: '{gdd.get('genre')}'")
                    print(f"  Controls: '{gdd.get('gameplay_loop', {}).get('controls')}'")
                    hitl_reached = True

            if hitl_reached:
                print("\n  Submitting HITL Approval...")
                await client.post(f"{base_url}/api/hitl/resume", json={
                    "session_id": session_id,
                    "action": "approved",
                    "feedback": ""
                })

                while not completed:
                    msg_raw = await ws.recv()
                    msg = json.loads(msg_raw)
                    msg_type = msg.get("type")
                    
                    if msg_type == "state_update":
                        logs = msg.get("logs", [])
                        if logs:
                            latest = logs[-1]
                            print(f"  [Log] [{latest.get('agent')}] {latest.get('message')}")
                    elif msg_type == "generation_completed":
                        print("\n>>> PRODUCTION COMPLETED <<<")
                        print(f"  Output URL: {msg.get('output_url')}")
                        completed = True
                    elif msg_type == "error":
                        print(f"  Error: {msg.get('message')}")
                        break

async def main():
    await test_topic("Tic Tac Toe Strategy")
    await test_topic("Labyrinth Maze Explorer")

if __name__ == "__main__":
    asyncio.run(main())
