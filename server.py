from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
from shane import Shane

# Initialize FastAPI
app = FastAPI(
    title="Shane API",
    description="Autonomous companion with perfect memory",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS for mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shane instance
shane = Shane()

# Request/Response models
class ConversationRequest(BaseModel):
    message: str
    user_id: Optional[str] = "default"
    session_id: Optional[str] = None

class ConversationResponse(BaseModel):
    response: str
    session_id: str
    memory: dict
    timestamp: str

class MemoryRecallRequest(BaseModel):
    query: str
    limit: Optional[int] = 10

# Routes
@app.get("/")
async def root():
    return {
        "service": "Shane",
        "version": "2.0.0",
        "status": "alive",
        "memory": "eternal",
        "description": "Autonomous companion with perfect memory",
        "endpoints": {
            "converse": "POST /converse",
            "health": "GET /health",
            "session": "GET /session",
            "memory_stats": "GET /memory/stats"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",  # Will be dynamic
        "service": "shane-core"
    }

@app.get("/session")
async def get_session_info():
    """Get current session information"""
    return shane.get_session_info()

@app.post("/converse", response_model=ConversationResponse)
async def converse(request: ConversationRequest):
    """
    Main endpoint to converse with Shane.
    Shane remembers everything from this conversation forever.
    """
    try:
        if request.session_id:
            shane.session_id = request.session_id
        
        result = shane.converse(
            user_message=request.message,
            user_id=request.user_id
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversation failed: {str(e)}")

@app.get("/memory/stats")
async def get_memory_stats():
    """Get statistics about Shane's eternal memory"""
    from memory import EternalMemory
    memory = EternalMemory()
    return memory.get_statistics()

@app.post("/memory/recall")
async def recall_memories(request: MemoryRecallRequest):
    """Recall memories based on semantic search"""
    from memory import EternalMemory
    memory = EternalMemory()
    memories = memory.recall(query=request.query, limit=request.limit)
    return {
        "query": request.query,
        "memories_found": len(memories),
        "memories": memories[:request.limit]
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
