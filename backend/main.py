from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from ai_service import GroqAIService

# Load environment variables
load_dotenv()

app = FastAPI(title="SEO Tools API", version="2.0.0")

# Initialize AI service
ai_service = GroqAIService()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

class EnhanceRequest(BaseModel):
    text: str
    enhancement_type: str = "general"  # seo, readability, general

class KeywordRequest(BaseModel):
    text: str
    target_count: int = 10

@app.post("/analyze")
async def analyze_content(request: TextRequest):
    """Analyze content for readability, SEO, and other metrics."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        result = await ai_service.analyze_content(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/enhance")
async def enhance_content(request: EnhanceRequest):
    """Enhance content for SEO, readability, or general improvement."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if request.enhancement_type not in ["seo", "readability", "general"]:
        raise HTTPException(status_code=400, detail="Invalid enhancement type")
    
    try:
        result = await ai_service.enhance_content(request.text, request.enhancement_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {str(e)}")

@app.post("/keywords")
async def suggest_keywords(request: KeywordRequest):
    """Generate keyword suggestions for content."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        result = await ai_service.suggest_keywords(request.text, request.target_count)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Keyword generation failed: {str(e)}")

@app.post("/humanize")
async def humanize_content(request: TextRequest):
    """Make AI-generated content more human-like."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        result = await ai_service.humanize_content(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Humanization failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    groq_configured = bool(os.getenv("GROQ_API_KEY"))
    return {
        "status": "healthy",
        "ai_service_available": groq_configured,
        "version": "2.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)