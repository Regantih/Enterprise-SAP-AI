from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil
from datetime import datetime
from pydantic import BaseModel

from src.api.routes import feedback, health
from src.core.engine import engine
from src.core.recruitment_engine import RecruitmentIntelligence


app = FastAPI(
    title="Enterprise AI Platform API",
    description="Backend for the Enterprise SAP AI Agents",
    version="3.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers (Feedback & Health only)
app.include_router(feedback.router, prefix="/api", tags=["Feedback"])
app.include_router(health.router, prefix="/api", tags=["Health"])

class ChatRequest(BaseModel):
    message: str

class RecruitmentSubmission(BaseModel):
    name: str # Candidate Name (Destination ID)
    role: str # Target Role
    origin_response: str # Answer to Protocol 1 (Interest/Drive)
    iq_response: str # Answer to Protocol 2 (IQ)
    eq_response: str # Answer to Protocol 3 (EQ)

class RecruitmentStore:
    """
    In-Memory Database for Live Recruitment.
    Stores real candidates submitted via the frontend.
    """
    def __init__(self):
        self.engine = RecruitmentIntelligence()
        self.candidates = []
        self.sessions = {} # Temporary storage for active interviews: {session_id: {data}}

    def add_segment(self, session_id: str, stage: str, video_path: str, metadata: dict):
        if session_id not in self.sessions:
            self.sessions[session_id] = {"segments": {}, "metadata": {}}
        
        self.sessions[session_id]["segments"][stage] = video_path
        # Update metadata if provided
        if metadata.get("name"): 
            self.sessions[session_id]["metadata"].update(metadata)
            
        print(f"Session {session_id}: Saved {stage} to {video_path}")
        return self.sessions[session_id]

    def submit_final_candidate(self, session_id: str):
        session = self.sessions.get(session_id)
        if not session:
            return None
            
        meta = session["metadata"]
        segments = session["segments"]
        
        # Default responses for MVP (since we don't have text anymore)
        # In a real system, we'd transcribe the videos.
        evaluation = self.engine.evaluate_candidate_4pillar(
            interest_response="Video Uploaded",
            iq_response="Video Uploaded",
            eq_response="Video Uploaded",
            drive_response="Video Uploaded"
        )
        
        record = {
            "id": f"ID-{len(self.candidates) + 1001}",
            "name": meta.get("name", "Unknown Candidate"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "role": meta.get("role", "Applicant"),
            "video_uplink": segments.get("protocol_04_drive", ""), # Main display video
            "segments": segments,
            "evaluation": evaluation
        }
        
        self.candidates.insert(0, record)
        # Cleanup session
        del self.sessions[session_id]
        return record

    def get_latest(self, count: int = 5):
        return self.candidates[:count]

# Global Store Instance
recruitment_system = RecruitmentStore()

# Ensure Uploads Directory Exists
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Submit Candidate Endpoint (Video Uplink)
@app.post("/api/recruitment/upload")
async def upload_video_segment(
    session_id: str = Form(...),
    stage: str = Form(...), # e.g., 'protocol_01_origin'
    name: str = Form(None),
    role: str = Form(None),
    video: UploadFile = File(...)
):
    """
    Receives a video segment for a specific stage.
    """
    # 1. Save Video
    file_location = f"{UPLOAD_DIR}/{session_id}_{stage}.webm"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(video.file, file_object)
    
    # 2. Add to Session
    metadata = {}
    if name: metadata["name"] = name
    if role: metadata["role"] = role
    
    recruitment_system.add_segment(session_id, stage, file_location, metadata)
    
    # 3. If Last Stage, Finalize
    result = None
    if stage == "protocol_04_drive":
         result = recruitment_system.submit_final_candidate(session_id)
    
    return {"status": "success", "stage": stage, "final_result": result}
    
@app.get("/api/recruitment/live")
async def get_recruitment_feed(count: int = 5):
    """Returns the REAL candidate list."""
    return {
        "status": "success",
        "timestamp": "LIVE",
        "data": recruitment_system.get_latest(count)
    }





class InterviewInteraction(BaseModel):
    session_id: str
    current_stage: str # "start", "protocol_01...", etc.
    message: str # Candidate's answer

# Global Recruiter Instance
from src.core.recruitment_engine import InteractiveRecruiter
interrogator = InteractiveRecruiter()

@app.post("/api/interview/interact")
async def interact_with_recruiter(interaction: InterviewInteraction):
    """
    Handles the chat turn. Use 'start' as current_stage for the initial greeting.
    """
    response = interrogator.interact(interaction.current_stage, interaction.message)
    return response

# Chat Endpoint (Using Reasoning Engine)
@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        response = engine.execute(request.message)
        
        if response["status"] == "success":
            # Format the output for the UI
            tool = response["tool_used"]
            
            if "message" in response:
                summary = response["message"]
                data = []
            else:
                data = response["data"]
                count = len(data) if isinstance(data, list) else 1
                
                # Generate a natural language summary
                summary = f"I executed `{tool}` and found {count} results."
                if count > 0 and isinstance(data, list):
                    first_item = data[0]
                    if "name" in first_item:
                        summary += f" Including '{first_item['name']}'."
                    elif "id" in first_item:
                        summary += f" Example ID: {first_item['id']}."
            
            return {
                "response": summary,
                "data": data,
                "trace": response["trace"],
                "tool": tool
            }
        else:
            return {
                "response": f"I encountered an issue: {response.get('message')}",
                "trace": response.get("trace"),
                "error": True
            }
            
    except Exception as e:
        # Log the error for debugging
        print(f"Error in chat endpoint: {e}")
        return {
            "response": f"System Error: {str(e)}",
            "trace": {"reasoning": ["System Error"]},
            "error": True
        }

# Demo Data Endpoint (Provides real sample IDs for demo buttons)
@app.get("/api/demo")
async def get_demo_data():
    from src.core.mock_sap import mock_db
    # Get sample data for demo buttons
    sample_po = mock_db.purchase_orders[0] if mock_db.purchase_orders else {}
    sample_vendor = mock_db.vendors[0] if mock_db.vendors else {}
    return {
        "sample_po_id": sample_po.get("id", "4500000"),
        "sample_vendor": sample_vendor.get("name", "Acme Corp"),
        "sample_plant": "Berlin"
    }



# Mount Static Files (Serve v7.html)
static_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/api")
async def root():
    return {"message": "Enterprise AI Platform API is running 🚀"}

