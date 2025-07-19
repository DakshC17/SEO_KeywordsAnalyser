import os
from groq import Groq
from typing import Dict, List, Any
import json
import re
import asyncio

class GroqAIService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=api_key)
        # Use supported Llama model
        self.model = "llama3-8b-8192"
    
    async def analyze_content(self, text: str) -> Dict[str, Any]:
        """Analyze content for readability, SEO metrics, and suggestions."""
        try:
            prompt = f"""Analyze the following content and provide detailed insights in JSON format:

Content: {text}

Provide your analysis in this exact JSON format:
{{
    "readability_score": 75.5,
    "word_count": 150,
    "sentence_count": 8,
    "avg_sentence_length": 18.75,
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "seo_score": 80,
    "improvements": ["improvement1", "improvement2"],
    "meta_description": "Generated meta description under 160 chars"
}}"""

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert content analyzer. Always respond with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
            )
            
            content = response.choices[0].message.content.strip()
            content = self._clean_json_response(content)
            
            try:
                result = json.loads(content)
                return {
                    "readability_score": result.get("readability_score", 50),
                    "word_count": len(text.split()),
                    "sentence_count": result.get("sentence_count", len(re.findall(r'[.!?]+', text))),
                    "keywords": result.get("keywords", [])[:10],
                    "seo_score": result.get("seo_score", 50),
                    "improvements": result.get("improvements", []),
                    "meta_description": result.get("meta_description", ""),
                    "success": True
                }
            except json.JSONDecodeError:
                return self._fallback_analysis(text)
                
        except Exception as e:
            return self._fallback_analysis(text, str(e))
    
    async def enhance_content(self, text: str, enhancement_type: str = "general") -> Dict[str, Any]:
        """Enhance content for SEO, readability, or engagement."""
        try:
            if enhancement_type == "seo":
                prompt = f"""Enhance the following content for better SEO while maintaining readability:

Original: {text}

Requirements:
- Improve keyword density naturally
- Add semantic keywords
- Optimize structure for search engines
- Maintain original meaning

Respond with JSON:
{{
    "enhanced_text": "improved content",
    "changes_made": ["change1", "change2"],
    "keywords_added": ["keyword1", "keyword2"]
}}"""
            
            elif enhancement_type == "readability":
                prompt = f"""Improve the readability of this content:

Original: {text}

Requirements:
- Simplify complex sentences
- Improve flow and structure
- Make it more engaging
- Keep the same meaning

Respond with JSON:
{{
    "enhanced_text": "improved content",
    "changes_made": ["change1", "change2"],
    "readability_improvements": ["improvement1", "improvement2"]
}}"""
            
            else:  # general enhancement
                prompt = f"""Enhance this content for better overall quality:

Original: {text}

Requirements:
- Improve clarity and engagement
- Better structure and flow
- More compelling language
- Professional tone

Respond with JSON:
{{
    "enhanced_text": "improved content",
    "changes_made": ["change1", "change2"],
    "improvements": ["improvement1", "improvement2"]
}}"""

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert content enhancer. Always respond with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=2000
                )
            )
            
            content = response.choices[0].message.content.strip()
            content = self._clean_json_response(content)
            
            try:
                result = json.loads(content)
                return {
                    "enhanced_text": result.get("enhanced_text", text),
                    "changes_made": result.get("changes_made", []),
                    "improvements": result.get("improvements", result.get("readability_improvements", result.get("keywords_added", []))),
                    "success": True
                }
            except json.JSONDecodeError:
                return {"enhanced_text": text, "changes_made": [], "improvements": [], "success": False}
                
        except Exception as e:
            return {"enhanced_text": text, "changes_made": [], "improvements": [f"Error: {str(e)}"], "success": False}
    
    async def suggest_keywords(self, text: str, target_count: int = 10) -> Dict[str, Any]:
        """Generate keyword suggestions for content."""
        try:
            prompt = f"""Generate {target_count} SEO keywords for this content:

Content: {text}

Provide keywords in this JSON format:
{{
    "primary_keywords": ["main keyword 1", "main keyword 2"],
    "secondary_keywords": ["related keyword 1", "related keyword 2"],
    "long_tail_keywords": ["long tail phrase 1", "long tail phrase 2"],
    "semantic_keywords": ["semantic keyword 1", "semantic keyword 2"]
}}"""

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an SEO keyword expert. Always respond with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.4,
                    max_tokens=800
                )
            )
            
            content = response.choices[0].message.content.strip()
            content = self._clean_json_response(content)
            
            try:
                result = json.loads(content)
                return {
                    "primary_keywords": result.get("primary_keywords", [])[:3],
                    "secondary_keywords": result.get("secondary_keywords", [])[:4],
                    "long_tail_keywords": result.get("long_tail_keywords", [])[:3],
                    "semantic_keywords": result.get("semantic_keywords", [])[:5],
                    "success": True
                }
            except json.JSONDecodeError:
                return self._fallback_keywords(text)
                
        except Exception as e:
            return self._fallback_keywords(text)
    
    async def humanize_content(self, text: str) -> Dict[str, Any]:
        """Make AI-generated content more human-like."""
        try:
            prompt = f"""Make this content sound more human and natural:

Original: {text}

Requirements:
- Add natural variations in sentence structure
- Include conversational elements
- Make it less robotic and more engaging
- Add personality while keeping professionalism
- Use contractions and natural language patterns

Respond with JSON:
{{
    "humanized_text": "more human-sounding content",
    "changes_made": ["change1", "change2"],
    "human_score": 85
}}"""

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert at making text sound natural and human. Always respond with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
            )
            
            content = response.choices[0].message.content.strip()
            content = self._clean_json_response(content)
            
            try:
                result = json.loads(content)
                return {
                    "humanized_text": result.get("humanized_text", text),
                    "changes_made": result.get("changes_made", []),
                    "human_score": result.get("human_score", 70),
                    "success": True
                }
            except json.JSONDecodeError:
                return {"humanized_text": text, "changes_made": [], "human_score": 50, "success": False}
                
        except Exception as e:
            return {"humanized_text": text, "changes_made": [f"Error: {str(e)}"], "human_score": 50, "success": False}
    
    def _clean_json_response(self, content: str) -> str:
        """Clean up AI response for JSON parsing."""
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'```\s*', '', content)
        content = content.strip()
        
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group()
        
        content = re.sub(r',\s*}', '}', content)
        content = re.sub(r',\s*]', ']', content)
        
        return content
    
    def _fallback_analysis(self, text: str, error: str = "") -> Dict[str, Any]:
        """Fallback analysis when AI fails."""
        words = text.split()
        sentences = re.findall(r'[.!?]+', text)
        
        return {
            "readability_score": 60,
            "word_count": len(words),
            "sentence_count": len(sentences),
            "keywords": self._extract_basic_keywords(text),
            "seo_score": 50,
            "improvements": ["AI analysis unavailable", f"Error: {error}" if error else ""],
            "meta_description": " ".join(words[:20]) + "...",
            "success": False
        }
    
    def _fallback_keywords(self, text: str) -> Dict[str, Any]:
        """Fallback keyword extraction."""
        keywords = self._extract_basic_keywords(text)
        return {
            "primary_keywords": keywords[:3],
            "secondary_keywords": keywords[3:7],
            "long_tail_keywords": [f"{keywords[0]} {keywords[1]}" if len(keywords) > 1 else ""],
            "semantic_keywords": keywords[7:12],
            "success": False
        }
    
    def _extract_basic_keywords(self, text: str) -> List[str]:
        """Extract basic keywords from text."""
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        common_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
            'how', 'its', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'text',
            'this', 'that', 'with', 'have', 'from', 'they', 'been', 'said', 'each',
            'which', 'their', 'time', 'will', 'about', 'would', 'there', 'could'
        }
        
        unique_words = []
        for word in words:
            if word not in common_words and word not in unique_words:
                unique_words.append(word)
        
        return unique_words[:15]