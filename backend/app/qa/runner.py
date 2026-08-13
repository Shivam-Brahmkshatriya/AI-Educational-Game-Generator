import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, List
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

async def run_playwright_qa_test(html_file_path: Path, timeout_sec: int = 8) -> Dict[str, Any]:
    """
    Executes automated headless browser testing on a generated Phaser 3 or HTML5 game index.html file.
    """
    abs_path = html_file_path.resolve()
    game_folder = abs_path.parent.name
    file_url = f"http://localhost:8000/games/{game_folder}/index.html"
    
    console_errors: List[str] = []
    page_errors: List[str] = []
    
    logger.info(f"Playwright QA booting Chromium for: {abs_path}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Listen for console errors
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type in ["error"] else None)
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        try:
            await page.goto(file_url, wait_until="domcontentloaded", timeout=10000)
            await asyncio.sleep(2.0)

            # Check for Phaser canvas OR HTML interactive board/container
            canvas = await page.query_selector("canvas")
            board = await page.query_selector("#board, .cell, #game-container")
            
            has_game_element = (canvas is not None) or (board is not None)

            # Simulate player inputs
            if canvas:
                await page.keyboard.press("ArrowLeft")
                await asyncio.sleep(0.3)
                await page.keyboard.press("ArrowRight")
                await asyncio.sleep(0.3)
                await page.keyboard.press("Space")
                await asyncio.sleep(0.5)
            elif board:
                first_cell = await page.query_selector(".cell, button")
                if first_cell:
                    await first_cell.click()
                    await asyncio.sleep(0.5)

            passed = (len(page_errors) == 0) and has_game_element
            
            return {
                "passed": passed,
                "has_canvas": has_game_element,
                "console_errors": console_errors,
                "page_errors": page_errors,
                "file_path": str(abs_path)
            }
        except Exception as e:
            logger.error(f"Playwright execution error: {e}")
            return {
                "passed": False,
                "has_canvas": False,
                "console_errors": console_errors,
                "page_errors": [str(e)],
                "file_path": str(abs_path)
            }
        finally:
            await browser.close()
