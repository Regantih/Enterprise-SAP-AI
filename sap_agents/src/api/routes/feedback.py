from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class FeedbackRequest(BaseModel):
    score: int
    messageId: str

@router.post("/feedback")
async def feedback_endpoint(request: FeedbackRequest):
    print(f"   [Feedback] 🗣️ User Feedback Received: {'👍' if request.score > 0 else '👎'} (ID: {request.messageId})")
    # In a real app, save to DB here
    return {"status": "success"}
