from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from .llm_client import review_code, review_code_stream
from .config import settings

app = FastAPI(title="AI Code Review Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    language: str

@app.post("/api/review")
async def review(request: CodeRequest):
    """Standard code review endpoint returning complete structured JSON."""
    if request.language.lower() not in settings.ALLOWED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language. Supported: {settings.ALLOWED_LANGUAGES}"
        )
    
    result = await review_code(request.code, request.language)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@app.post("/api/review/stream")
async def review_stream(request: CodeRequest):
    """Streaming endpoint for real-time token output."""
    if request.language.lower() not in settings.ALLOWED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language. Supported: {settings.ALLOWED_LANGUAGES}"
        )
    
    return StreamingResponse(
        review_code_stream(request.code, request.language),
        media_type="text/plain"
    )

@app.get("/health")
async def health():
    """Deployment health check endpoint."""
    return {"status": "healthy", "service": "code-review-backend"}