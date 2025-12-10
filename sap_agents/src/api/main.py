from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pydantic import BaseModel

from src.api.routes import feedback, health
from src.core.engine import engine

class ChatRequest(BaseModel):
    message: str

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

