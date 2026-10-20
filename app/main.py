from fastapi import FastAPI
from app.api.evaluate import router as eval_router
from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

app.include_router(eval_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Automated LLM Evaluation Pipeline API"}