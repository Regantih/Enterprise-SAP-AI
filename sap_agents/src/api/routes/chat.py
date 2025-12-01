from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.agents.orchestrator import orchestrator
from src.services.human_handoff import confidence_engine

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # 1. Get response from Orchestrator (already includes audit info)
        final_response, transaction_id = orchestrator.run(request.message)
        
        return {
            "response": final_response,
            "trace": orchestrator.get_trace()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
