import time
import google.generativeai as genai
from app.core.config import settings
from app.models.schemas import TestCase, EvaluationResult
from app.services.metrics import calculate_deterministic_score

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

async def run_evaluation_pipeline(model_name: str, test_case: TestCase) -> EvaluationResult:
    start_time = time.time()
    
    # Simulate or call actual model generation here
    # For demonstration, using Gemini or mock response
    generated_response = f"Simulated response from {model_name} for prompt: {test_case.prompt}"
    
    latency = time.time() - start_time
    token_count = len(generated_response.split()) * 2  # Approximate token metric
    
    # 1. Deterministic Evaluation
    det_score = calculate_deterministic_score(generated_response, test_case.expected_keywords)
    
    # 2. LLM-as-a-Judge Evaluation (Mocked or API call)
    faithfulness_score = 0.95
    relevance_score = 0.90
    
    return EvaluationResult(
        test_id=test_case.test_id,
        model_name=model_name,
        response=generated_response,
        latency_seconds=round(latency, 4),
        token_count=token_count,
        deterministic_score=det_score,
        faithfulness_score=faithfulness_score,
        relevance_score=relevance_score,
        metadata={"evaluator": "gemini-1.5-flash-judge"}
    )
