from fastapi import HTTPException
from app.models.schemas import EvaluationRequest, EvaluationResult
from app.services.evaluator import run_evaluation_pipeline
from app.core.database import get_database
import time

async def process_evaluation_request(payload: EvaluationRequest) -> dict:
    db = get_database()
    results = []
    start_time = time.time()
    
    for test_case in payload.test_cases:
        try:
            eval_result: EvaluationResult = await run_evaluation_pipeline(
                model_name=payload.model_name,
                test_case=test_case
            )
            results.append(eval_result.model_dump())
            
            # Persist to MongoDB
            await db.evaluation_logs.insert_one(eval_result.model_dump())
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error evaluating test_id {test_case.test_id}: {str(e)}")
            
    total_duration = time.time() - start_time
    
    return {
        "status": "success",
        "model_name": payload.model_name,
        "total_evaluated": len(results),
        "total_duration_seconds": round(total_duration, 2),
        "results": results
    }
