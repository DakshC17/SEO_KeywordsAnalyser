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
        # Use Mistral model as requested
        self.model = "mixtral-8x7b-32768"  # Mistral model via Groq
    
    async def enhance_content_for_seo(self, text: str, keywords: List[str] = None) -> Dict[str, Any]:
        """Enhance content for better SEO using Mistral AI through Groq."""
        try:
            keywords_text = ", ".join(keywords) if keywords else "relevant SEO keywords"
            
            prompt = f"""You are an expert SEO content optimizer. Analyze and enhance the following text for better search engine optimization while maintaining readability and natural flow.

Original Text:
{text}

Target Keywords (if provided): {keywords_text}

Please enhance this content and provide your response in the following JSON format only (no additional text):

{{
    "enhanced_text": "your improved version of the text with better SEO optimization",
    "suggested_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "seo_improvements": ["specific improvement 1", "specific improvement 2", "specific improvement 3"],
    "structure_recommendations": ["structure tip 1", "structure tip 2", "structure tip 3"]
}}

Requirements for enhancement:
- Improve keyword density naturally
- Enhance readability and flow
- Add relevant semantic keywords
- Improve sentence structure for SEO
- Maintain the original meaning and tone"""

            # Use sync call in async function with run_in_executor
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert SEO content optimizer. Always respond with valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,  # Lower temperature for more consistent output
                    max_tokens=2000
                )
            )
            
            # Parse the JSON response
            content = response.choices[0].message.content.strip()
            
            # Clean up the response to ensure valid JSON
            content = self._clean_json_response(content)
            
            try:
                result = json.loads(content)
                
                # Validate the response structure
                if not isinstance(result, dict):
                    raise ValueError("Response is not a valid dictionary")
                
                return {
                    "enhanced_text": result.get("enhanced_text", text),
                    "suggested_keywords": result.get("suggested_keywords", [])[:8],  # Limit to 8
                    "seo_improvements": result.get("seo_improvements", [])[:5],  # Limit to 5
                    "structure_recommendations": result.get("structure_recommendations", [])[:5],  # Limit to 5
                    "success": True
                }
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw response: {content}")
                # Fallback if JSON parsing fails
                return self._create_fallback_enhancement(text, content)
                
        except Exception as e:
            print(f"AI Enhancement Error: {str(e)}")
            return {
                "enhanced_text": text,
                "suggested_keywords": self._extract_basic_keywords(text),
                "seo_improvements": [f"AI service temporarily unavailable: {str(e)}"],
                "structure_recommendations": ["Please try again later"],
                "success": False,
                "error": str(e)
            }
    
    def _clean_json_response(self, content: str) -> str:
        """Clean up the AI response to ensure valid JSON."""
        # Remove any markdown code blocks
        content = re.sub(r'```json\s*', '', content)
        content = re.sub(r'```\s*', '', content)
        
        # Remove any leading/trailing whitespace
        content = content.strip()
        
        # Try to extract JSON from the response if it's embedded in text
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group()
        
        # Fix common JSON issues
        content = re.sub(r',\s*}', '}', content)  # Remove trailing commas
        content = re.sub(r',\s*]', ']', content)  # Remove trailing commas in arrays
        
        return content
    
    def _extract_basic_keywords(self, text: str) -> List[str]:
        """Extract basic keywords from text as fallback."""
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        common_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 
            'how', 'its', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'text', 
            'this', 'that', 'with', 'have', 'from', 'they', 'been', 'said', 'each', 
            'which', 'their', 'time', 'will', 'about', 'would', 'there', 'could',
            'other', 'after', 'first', 'well', 'water', 'than', 'many', 'where',
            'some', 'what', 'your', 'when', 'here', 'more', 'just', 'like', 'long',
            'make', 'thing', 'look', 'right', 'come', 'good', 'very', 'much'
        }
        
        # Get unique meaningful words
        unique_words = []
        for word in words:
            if word not in common_words and word not in unique_words:
                unique_words.append(word)
        
        return unique_words[:8]
    
    def _create_fallback_enhancement(self, original_text: str, ai_response: str) -> Dict[str, Any]:
        """Create a fallback response when JSON parsing fails."""
        print(f"Creating fallback enhancement. AI Response: {ai_response[:200]}...")
        
        # Try to extract some useful information from the response
        lines = [line.strip() for line in ai_response.split('\n') if line.strip()]
        
        keywords = self._extract_basic_keywords(original_text)
        improvements = [
            "Consider adding more relevant keywords naturally",
            "Improve paragraph structure for better readability",
            "Add subheadings to organize content",
            "Include call-to-action phrases"
        ]
        recommendations = [
            "Use shorter sentences for better readability",
            "Add bullet points where appropriate",
            "Include relevant internal and external links",
            "Optimize for featured snippets"
        ]
        
        return {
            "enhanced_text": original_text,
            "suggested_keywords": keywords,
            "seo_improvements": improvements,
            "structure_recommendations": recommendations,
            "success": False,
            "raw_response": ai_response[:500]  # Limit raw response length
        }

    async def generate_meta_description(self, text: str, max_length: int = 160) -> str:
        """Generate SEO-optimized meta description."""
        try:
            prompt = f"""Create a compelling SEO meta description for the following content. 
The meta description must be exactly {max_length} characters or less, include relevant keywords, and encourage clicks.

Content: {text[:400]}

Respond with ONLY the meta description text, no quotes, no additional formatting."""

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert at writing SEO meta descriptions. Respond with only the meta description text."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.4,
                    max_tokens=60
                )
            )
            
            meta_description = response.choices[0].message.content.strip()
            
            # Clean up the response
            meta_description = meta_description.strip('"\'`')
            meta_description = re.sub(r'^Meta description:\s*', '', meta_description, flags=re.IGNORECASE)
            
            # Ensure it's within character limit
            if len(meta_description) > max_length:
                # Try to cut at word boundary
                words = meta_description[:max_length-3].split()
                if len(words) > 1:
                    meta_description = " ".join(words[:-1]) + "..."
                else:
                    meta_description = meta_description[:max_length-3] + "..."
            
            return meta_description
            
        except Exception as e:
            print(f"Meta description generation error: {e}")
            # Fallback meta description
            words = text.split()[:20]
            fallback = " ".join(words)
            if len(fallback) > max_length:
                fallback = fallback[:max_length-3] + "..."
            return fallback

    async def suggest_title_variations(self, text: str, current_title: str = None) -> List[str]:
        """Generate SEO-friendly title variations."""
        try:
            prompt = f"""Based on the following content, suggest exactly 5 SEO-optimized title variations.

Content: {text[:300]}
Current title: {current_title or "None provided"}

Requirements for each title:
- 50-60 characters long
- Include relevant keywords
- Be compelling and click-worthy
- Follow SEO best practices

Respond with exactly 5 titles, one per line, no numbering, no quotes, no additional text."""

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert at creating SEO-optimized titles. Respond with exactly 5 titles, one per line."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.6,
                    max_tokens=200
                )
            )
            
            titles = response.choices[0].message.content.strip().split('\n')
            cleaned_titles = []
            
            for title in titles:
                title = title.strip()
                # Remove numbering, quotes, and extra formatting
                title = re.sub(r'^\d+[\.\)\-\:]\s*', '', title)
                title = title.strip('"\'`')
                title = re.sub(r'^Title\s*\d*[\:\-]?\s*', '', title, flags=re.IGNORECASE)
                
                if title and len(title) > 10 and len(title) <= 70:
                    cleaned_titles.append(title)
            
            # Ensure we have at least some titles
            if not cleaned_titles:
                cleaned_titles = [
                    "SEO-Optimized Content for Better Rankings",
                    "Expert Guide to Content Optimization",
                    "Boost Your Search Rankings with Quality Content",
                    "Professional Content Enhancement Tips",
                    "Advanced SEO Strategies for Content"
                ]
            
            return cleaned_titles[:5]
            
        except Exception as e:
            print(f"Title generation error: {e}")
            return [
                "SEO-Optimized Content for Better Rankings",
                "Expert Guide to Content Optimization",
                "Boost Your Search Rankings Today",
                "Professional Content Enhancement",
                "Advanced SEO Content Strategy"
            ]