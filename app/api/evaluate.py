from fastapi import APIRouter, status
from app.models.schemas import EvaluationRequest
from app.controllers.eval_controller import process_evaluation_request

router = APIRouter(prefix="/evaluate", tags=["Evaluation Pipeline"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def evaluate_outputs(payload: EvaluationRequest):
    return await process_evaluation_request(payload)
