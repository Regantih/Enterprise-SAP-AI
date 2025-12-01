from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from src.api.routes import chat, feedback, health

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

# Include Routers
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(feedback.router, prefix="/api", tags=["Feedback"])
app.include_router(health.router, prefix="/api", tags=["Health"])

# Mount Static Files (Serve v6.html)
static_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/api")
async def root():
    return {"message": "Enterprise AI Platform API is running 🚀"}
