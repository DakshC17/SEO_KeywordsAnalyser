import streamlit as st
import requests
import json
from typing import Dict, List, Any
import re

# Configure Streamlit page
st.set_page_config(
    page_title="SEO Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend API URL
API_BASE_URL = "http://localhost:8000"

def main():
    st.title("🔍 SEO Content Analyzer")
    st.markdown("---")
    
    # Initialize session state
    if 'original_text' not in st.session_state:
        st.session_state.original_text = ""
    if 'modified_text' not in st.session_state:
        st.session_state.modified_text = ""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'inserted_keywords' not in st.session_state:
        st.session_state.inserted_keywords = set()
    if 'ai_enhancement_results' not in st.session_state:
        st.session_state.ai_enhancement_results = None

    # Sidebar for controls
    with st.sidebar:
        st.header("📊 Analysis Results")
        
        if st.session_state.analysis_results:
            display_analysis_sidebar(st.session_state.analysis_results)
        
        # AI Enhancement Results
        if st.session_state.ai_enhancement_results:
            st.markdown("---")
            display_ai_results_sidebar(st.session_state.ai_enhancement_results)
        
        st.markdown("---")
        
        if st.button("🔄 Reset All", type="secondary", use_container_width=True):
            reset_session_state()
            st.rerun()

    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("✏️ Input Content")
        
        # Text input area
        user_text = st.text_area(
            "Enter your content (blog, tweet, caption, etc.):",
            value=st.session_state.original_text,
            height=300,
            placeholder="Paste your content here for SEO analysis..."
        )
        
        # Update session state
        if user_text != st.session_state.original_text:
            st.session_state.original_text = user_text
            st.session_state.modified_text = user_text
        
        # Action buttons
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        with col_btn1:
            if st.button("🔍 Analyze", type="primary", use_container_width=True):
                if user_text.strip():
                    analyze_content_handler(user_text)
                else:
                    st.error("Please enter some content to analyze.")
        
        with col_btn2:
            if st.button("🤖 Enhance with AI", type="secondary", use_container_width=True):
                if user_text.strip():
                    enhance_with_ai_handler(user_text)
                else:
                    st.error("Please enter some content to enhance.")
        
        with col_btn3:
            if st.button("📄 Clear", use_container_width=True):
                st.session_state.original_text = ""
                st.session_state.modified_text = ""
                st.rerun()

    with col2:
        st.subheader("📝 Optimized Content")
        
        if st.session_state.modified_text:
            # Display modified text with highlighted keywords
            highlighted_text = highlight_inserted_keywords(
                st.session_state.modified_text, 
                st.session_state.inserted_keywords
            )
            
            st.markdown(
                f"""
                <div style="
                    background-color: #f8f9fa;
                    padding: 1rem;
                    border-radius: 8px;
                    border: 1px solid #e9ecef;
                    height: 300px;
                    overflow-y: auto;
                ">
                {highlighted_text}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Export button
            if st.button("📥 Download Optimized Content", use_container_width=True):
                st.download_button(
                    label="Download as TXT",
                    data=st.session_state.modified_text,
                    file_name="optimized_content.txt",
                    mime="text/plain"
                )
        else:
            st.info("Your optimized content will appear here after analysis.")

    # Keywords section
    if st.session_state.analysis_results:
        st.markdown("---")
        display_keywords_section(st.session_state.analysis_results.get('keywords', []))
    
    # AI Enhancement Results
    if st.session_state.ai_enhancement_results:
        st.markdown("---")
        display_ai_enhancement_results(st.session_state.ai_enhancement_results)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def analyze_content_api(text: str) -> Dict[str, Any]:
    """Analyze content using the FastAPI backend (cached version)."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json={"text": text},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the analysis server. Please ensure the backend is running.")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Analysis timed out. Please try again.")
        return None
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        return None

def analyze_content_handler(text: str):
    """Analyze content and update session state."""
    results = analyze_content_api(text)
    if results:
        st.session_state.analysis_results = results
        st.success("✅ Analysis complete!")
        st.rerun()

def enhance_with_ai_handler(text: str):
    """Enhance content with AI and update session state."""
    try:
        with st.spinner("🤖 Enhancing content with AI..."):
            # Get current keywords if available
            keywords = []
            if st.session_state.analysis_results:
                keywords = [kw["keyword"] for kw in st.session_state.analysis_results.get("keywords", [])]
            
            response = requests.post(
                f"{API_BASE_URL}/enhance_with_ai",
                json={"text": text, "keywords": keywords},
                timeout=60
            )
            response.raise_for_status()
            
            results = response.json()
            st.session_state.ai_enhancement_results = results
            
            # Update the modified text with enhanced version
            if results.get("success") and results.get("enhanced_text"):
                st.session_state.modified_text = results["enhanced_text"]
            
            st.success("✅ AI enhancement complete!")
            st.rerun()
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to AI service. Please ensure the backend is running.")
    except requests.exceptions.Timeout:
        st.error("⏱️ AI enhancement timed out. Please try again.")
    except Exception as e:
        st.error(f"❌ AI enhancement failed: {str(e)}")

def insert_keyword(keyword: str):
    """Insert keyword into the text."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/insert_keyword",
            json={
                "text": st.session_state.modified_text,
                "keyword": keyword
            },
            timeout=10
        )
        response.raise_for_status()
        
        result = response.json()
        st.session_state.modified_text = result['modified_text']
        st.session_state.inserted_keywords.add(keyword.lower())
        
        st.success(f"✅ Keyword '{keyword}' inserted successfully!")
        st.rerun()
    
    except Exception as e:
        st.error(f"❌ Failed to insert keyword: {str(e)}")

def display_analysis_sidebar(results: Dict[str, Any]):
    """Display analysis results in sidebar."""
    
    # Readability Score
    readability = results.get('readability_score', 0)
    st.metric("📖 Readability Score", f"{readability:.1f}/100")
    
    # Readability interpretation
    if readability >= 70:
        st.success("🟢 Very Easy to Read")
    elif readability >= 50:
        st.warning("🟡 Moderately Easy")
    else:
        st.error("🔴 Difficult to Read")
    
    # Word Count
    word_count = results.get('word_count', 0)
    st.metric("📝 Word Count", word_count)
    
    # SEO Score (calculated based on readability and keyword usage)
    seo_score = min(100, max(0, readability * 0.7 + len(results.get('keywords', [])) * 2))
    st.metric("🎯 SEO Score", f"{seo_score:.0f}/100")

def display_ai_results_sidebar(results: Dict[str, Any]):
    """Display AI enhancement results in sidebar."""
    st.header("🤖 AI Enhancement")
    
    if results.get("success"):
        st.success("✅ AI Enhancement Successful")
    else:
        st.warning("⚠️ AI Enhancement Partial")
    
    # Show number of suggestions
    improvements = len(results.get("seo_improvements", []))
    recommendations = len(results.get("structure_recommendations", []))
    suggested_keywords = len(results.get("suggested_keywords", []))
    
    st.metric("💡 SEO Improvements", improvements)
    st.metric("📋 Structure Tips", recommendations)
    st.metric("🔑 AI Keywords", suggested_keywords)

def display_keywords_section(keywords: List[Dict[str, Any]]):
    """Display keywords with insert buttons."""
    st.subheader("🎯 Recommended Keywords")
    
    if not keywords:
        st.info("No keywords found. Try analyzing some content first.")
        return
    
    # Display keywords in a nice layout
    cols = st.columns(2)
    
    for i, keyword_data in enumerate(keywords):
        col_idx = i % 2
        
        with cols[col_idx]:
            keyword = keyword_data.get('keyword', '')
            weight = keyword_data.get('weight', 0)
            relevance = keyword_data.get('relevance', 0)
            
            # Create a card-like display
            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        background-color: #ffffff;
                        padding: 1rem;
                        border-radius: 8px;
                        border: 1px solid #e9ecef;
                        margin-bottom: 0.5rem;
                    ">
                        <strong>{keyword}</strong><br>
                        <small>Weight: {weight:.2f} | Relevance: {relevance:.2f}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Insert button and status
                if keyword.lower() not in st.session_state.inserted_keywords:
                    if st.button(f"➕ Insert '{keyword}'", key=f"insert_{keyword}_{i}"):
                        insert_keyword(keyword)
                else:
                    # Use a container instead of st.success with key
                    with st.container():
                        st.markdown(
                            '<div style="color: #28a745; font-weight: bold;">✅ Already inserted</div>',
                            unsafe_allow_html=True
                        )

def display_ai_enhancement_results(results: Dict[str, Any]):
    """Display AI enhancement results."""
    st.subheader("🤖 AI Enhancement Results")
    
    tabs = st.tabs(["📝 Suggestions", "🔑 Keywords", "📊 Meta & Titles"])
    
    with tabs[0]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**💡 SEO Improvements:**")
            improvements = results.get("seo_improvements", [])
            for improvement in improvements:
                st.write(f"• {improvement}")
        
        with col2:
            st.write("**📋 Structure Recommendations:**")
            recommendations = results.get("structure_recommendations", [])
            for recommendation in recommendations:
                st.write(f"• {recommendation}")
    
    with tabs[1]:
        st.write("**🔑 AI Suggested Keywords:**")
        ai_keywords = results.get("suggested_keywords", [])
        
        if ai_keywords:
            # Display in columns
            cols = st.columns(3)
            for i, keyword in enumerate(ai_keywords):
                col_idx = i % 3
                with cols[col_idx]:
                    if st.button(f"➕ {keyword}", key=f"ai_keyword_{i}"):
                        insert_keyword(keyword)
        else:
            st.info("No AI keywords generated.")
    
    with tabs[2]:
        # Meta Description
        meta_desc = results.get("meta_description", "")
        if meta_desc:
            st.write("**📄 Generated Meta Description:**")
            st.code(meta_desc, language=None)
            st.caption(f"Length: {len(meta_desc)} characters")
        
        # Title Suggestions
        titles = results.get("title_suggestions", [])
        if titles:
            st.write("**📰 Title Suggestions:**")
            for i, title in enumerate(titles):
                st.write(f"{i+1}. {title}")

def highlight_inserted_keywords(text: str, inserted_keywords: set) -> str:
    """Highlight inserted keywords in the text."""
    if not inserted_keywords:
        return text.replace('\n', '<br>')
    
    highlighted_text = text
    
    for keyword in inserted_keywords:
        # Use regex to find whole words only
        pattern = r'\b' + re.escape(keyword) + r'\b'
        highlighted_text = re.sub(
            pattern,
            f'<mark style="background-color: #fff3cd; padding: 2px 4px; border-radius: 3px;">{keyword}</mark>',
            highlighted_text,
            flags=re.IGNORECASE
        )
    
    return highlighted_text.replace('\n', '<br>')

def reset_session_state():
    """Reset all session state variables."""
    st.session_state.original_text = ""
    st.session_state.modified_text = ""
    st.session_state.analysis_results = None
    st.session_state.inserted_keywords = set()
    st.session_state.ai_enhancement_results = None

if __name__ == "__main__":
    main()  