from typing import TypedDict, List, Dict, Any, Optional

class GameState(TypedDict):
    topic: str
    research_facts: List[str]
    mechanics_idea: str
    narrative_idea: str
    educational_idea: str
    gdd: Dict[str, Any]
    critic_approved: bool
    critic_feedback: str
    hitl_status: str  # "pending", "approved", "rejected"
    user_feedback: str
    asset_palette: Dict[str, Any]
    generated_code: str
    qa_passed: bool
    qa_report: Dict[str, Any]
    qa_iterations: int
    output_path: str
    logs: List[Dict[str, Any]]
