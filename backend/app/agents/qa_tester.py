import logging
from typing import Dict, Any
from app.agents.base import call_ollama, extract_json

logger = logging.getLogger(__name__)

async def run_qa_tester(qa_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes Playwright test results and formulates diagnostic bug reports if errors occurred.
    """
    passed = qa_result.get("passed", False)
    has_canvas = qa_result.get("has_canvas", False)
    page_errors = qa_result.get("page_errors", [])
    console_errors = qa_result.get("console_errors", [])

    if passed and has_canvas:
        logger.info("QA Tester: Game passed all browser automated checks!")
        return {
            "passed": True,
            "errors": [],
            "summary": "Game booted successfully with canvas rendering and zero runtime uncaught exceptions."
        }

    # Formulate fix prompt for Gemma LLM
    errors = page_errors + [e for e in console_errors if "error" in e.lower() or "uncaught" in e.lower()]
    if not errors and not has_canvas:
        errors = ["Phaser canvas element failed to render on DOM load."]

    prompt = f"""
You are the Automated QA Engineer.
Analyze this Playwright test failure for a Phaser.js game:

Canvas Rendered: {has_canvas}
Errors Encountered:
{errors}

Provide a concise bug report and exact fix instructions for the Developer Agent.
Output JSON:
```json
{{
  "passed": false,
  "errors": {errors},
  "summary": "Brief explanation of the bug",
  "recommended_fix": "Exact code fix instructions"
}}
```
"""
    system_prompt = "You are a QA automation diagnostic agent. Return JSON."
    
    response = await call_ollama(prompt, system_prompt=system_prompt, json_mode=True)
    report = extract_json(response)
    
    if "passed" not in report:
        report = {
            "passed": False,
            "errors": errors,
            "summary": "Runtime error detected during Playwright startup.",
            "recommended_fix": "Fix variable scoping and ensure Phaser physics sprites use valid texture keys."
        }

    logger.warning(f"QA Tester reported failure: {report.get('summary')}")
    return report
