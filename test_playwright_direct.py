import asyncio
from pathlib import Path
from app.qa.runner import run_playwright_qa_test

async def main():
    path = Path("output/games/photosynthesis_quest/index.html")
    res = await run_playwright_qa_test(path)
    print("Direct Playwright QA Test Result:")
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
