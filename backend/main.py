from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import re
from typing import List, Dict, Any, Optional
from ai_service import GroqAIService

# Load environment variables
load_dotenv()

app = FastAPI(title="SEO Analyzer API", version="1.0.0")

# Initialize AI service
ai_service = GroqAIService()

# Add CORS middleware for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextAnalysisRequest(BaseModel):
    text: str

class KeywordInsertRequest(BaseModel):
    text: str
    keyword: str

class AIEnhanceRequest(BaseModel):
    text: str
    keywords: Optional[List[str]] = None

class AnalysisResponse(BaseModel):
    readability_score: float
    keywords: List[Dict[str, Any]]
    word_count: int

class AIEnhanceResponse(BaseModel):
    enhanced_text: str
    suggested_keywords: List[str]
    seo_improvements: List[str]
    structure_recommendations: List[str]
    meta_description: str
    title_suggestions: List[str]
    success: bool

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """Analyze text for SEO metrics using Razor API."""
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        # Calculate readability score (simplified Flesch Reading Ease formula)
        readability_score = calculate_readability(request.text)
        
        # Get keywords from Razor API
        keywords = await get_keywords_from_razor(request.text)
        
        # Calculate word count
        word_count = len(request.text.split())
        
        return AnalysisResponse(
            readability_score=readability_score,
            keywords=keywords,
            word_count=word_count
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/insert_keyword")
async def insert_keyword(request: KeywordInsertRequest):
    """Insert keyword intelligently into text."""
    if not request.text or not request.keyword:
        raise HTTPException(status_code=400, detail="Text and keyword cannot be empty")
    
    try:
        from keyword_utils import insert_keyword_intelligently
        modified_text = insert_keyword_intelligently(request.text, request.keyword)
        return {"modified_text": modified_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Keyword insertion failed: {str(e)}")

@app.post("/enhance_with_ai", response_model=AIEnhanceResponse)
async def enhance_with_ai(request: AIEnhanceRequest):
    """Enhance content using Mistral AI through Groq."""
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Check if GROQ API key is available
    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(status_code=500, detail="AI service not configured. Please add GROQ_API_KEY to environment variables.")
    
    try:
        # Enhance content with AI
        enhancement_result = await ai_service.enhance_content_for_seo(request.text, request.keywords)
        
        # Generate meta description
        meta_description = await ai_service.generate_meta_description(request.text)
        
        # Generate title suggestions
        title_suggestions = await ai_service.suggest_title_variations(request.text)
        
        return AIEnhanceResponse(
            enhanced_text=enhancement_result.get("enhanced_text", request.text),
            suggested_keywords=enhancement_result.get("suggested_keywords", []),
            seo_improvements=enhancement_result.get("seo_improvements", []),
            structure_recommendations=enhancement_result.get("structure_recommendations", []),
            meta_description=meta_description,
            title_suggestions=title_suggestions,
            success=enhancement_result.get("success", False)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI enhancement failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    groq_configured = bool(os.getenv("GROQ_API_KEY"))
    return {
        "status": "healthy",
        "ai_service_available": groq_configured,
        "version": "1.0.0"
    }

def calculate_readability(text: str) -> float:
    """Calculate a simplified readability score."""
    if not text.strip():
        return 0.0
    
    # Count sentences (look for sentence endings)
    sentences = len(re.findall(r'[.!?]+', text))
    if sentences == 0:
        sentences = 1  # Assume at least one sentence
    
    # Count words
    words = text.split()
    word_count = len(words)
    
    if word_count == 0:
        return 0.0
    
    # Count syllables
    total_syllables = 0
    for word in words:
        syllables = count_syllables(word)
        total_syllables += syllables
    
    # Flesch Reading Ease formula
    # Score = 206.835 - (1.015 × ASL) - (84.6 × ASW)
    # ASL = Average Sentence Length (words per sentence)
    # ASW = Average Syllables per Word
    
    asl = word_count / sentences
    asw = total_syllables / word_count
    
    score = 206.835 - (1.015 * asl) - (84.6 * asw)
    
    # Ensure score is between 0 and 100
    return max(0.0, min(100.0, score))

def count_syllables(word: str) -> int:
    """Count syllables in a word (simplified approach)."""
    word = word.lower().strip('.,!?;:"()[]')
    
    if not word:
        return 1
    
    vowels = "aeiouy"
    syllable_count = 0
    prev_was_vowel = False
    
    for i, char in enumerate(word):
        if char in vowels:
            if not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = True
        else:
            prev_was_vowel = False
    
    # Handle silent 'e'
    if word.endswith('e') and syllable_count > 1:
        syllable_count -= 1
    
    # Every word has at least one syllable
    return max(1, syllable_count)

async def get_keywords_from_razor(text: str) -> List[Dict[str, Any]]:
    """Get keyword suggestions from Razor API."""
    razor_api_key = os.getenv("RAZOR_API_KEY")
    
    if not razor_api_key:
        # Fallback to mock data if no API key
        return generate_mock_keywords(text)
    
    try:
        # Replace with actual Razor API endpoint
        headers = {
            "Authorization": f"Bearer {razor_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text,
            "max_keywords": 10
        }
        
        # Mock response - replace with actual Razor API call
        # response = requests.post("https://api.razor.com/keywords", 
        #                         json=payload, headers=headers, timeout=10)
        # response.raise_for_status()
        # return response.json().get("keywords", [])
        
        return generate_mock_keywords(text)
    
    except Exception as e:
        print(f"Razor API error: {e}")
        return generate_mock_keywords(text)

def generate_mock_keywords(text: str) -> List[Dict[str, Any]]:
    """Generate mock keywords for testing."""
    if not text.strip():
        return []
    
    words = text.lower().split()
    common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'a', 'an', 'this', 'that', 'it', 'from', 'as', 'be', 'have', 'has', 'had', 'will', 'would', 'could', 'should'}
    
    # Get unique words, filter out common words and short words
    unique_words = []
    for word in words:
        cleaned_word = word.strip('.,!?;:"()[]')
        if (len(cleaned_word) >= 3 and 
            cleaned_word not in common_words and 
            cleaned_word not in unique_words):
            unique_words.append(cleaned_word)
    
    # Create mock keyword suggestions
    keywords = []
    for i, word in enumerate(unique_words[:8]):
        keywords.append({
            "keyword": word,
            "weight": round(0.9 - i * 0.1, 2),
            "relevance": round(0.8 - i * 0.05, 2),
            "difficulty": round(0.3 + i * 0.1, 2)
        })
    
    return keywords

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)