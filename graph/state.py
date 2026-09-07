from typing import TypedDict, List, Dict, Any, Optional

class Evidence(TypedDict):
    title: str
    body: str
    url: Optional[str]
    source: str

class LogEntry(TypedDict):
    step: str
    timestamp: str
    message: str
    details: Optional[Dict[str, Any]]

class ResearchState(TypedDict):
    topic: str
    research_queries: List[str]
    raw_evidence: List[Evidence]
    draft: str
    final_report: str
    quality_score: float
    revision_count: int
    execution_logs: List[LogEntry]
    status: str
