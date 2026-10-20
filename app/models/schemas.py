from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class TestCase(BaseModel):
    test_id: str
    prompt: str
    ground_truth: Optional[str] = None
    expected_keywords: List[str] = Field(default_factory=list)

class EvaluationRequest(BaseModel):
    model_name: str
    test_cases: List[TestCase]

class EvaluationResult(BaseModel):
    test_id: str
    model_name: str
    response: str
    latency_seconds: float
    token_count: int
    deterministic_score: float  # Keyword/exact match score
    faithfulness_score: float   # LLM-as-a-Judge score (0.0 to 1.0)
    relevance_score: float      # LLM-as-a-Judge score (0.0 to 1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)