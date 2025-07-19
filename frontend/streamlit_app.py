import streamlit as st
import requests
import json
from typing import Dict, Any

# Configure Streamlit page
st.set_page_config(
    page_title="SEO Tools Suite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend API URL
API_BASE_URL = "http://localhost:8000"

def main():
    st.title("🚀 SEO Tools Suite")
    st.markdown("*Your complete toolkit for content optimization*")
    st.markdown("---")
    
    # Sidebar for tool selection
    with st.sidebar:
        st.header("🛠️ Select Tool")
        
        tool_option = st.selectbox(
            "Choose what you want to do:",
            [
                "🔍 Analyze Content",
                "✨ Enhancify Content", 
                "🎯 Keyword Suggester",
                "🤖 AI Humanizer"
            ]
        )
        
        st.markdown("---")
        st.info("💡 **Tip**: Choose the tool that best fits your current needs!")
    
    # Route to different tools based on selection
    if tool_option == "🔍 Analyze Content":
        show_analyze_tool()
    elif tool_option == "✨ Enhancify Content":
        show_enhance_tool()
    elif tool_option == "🎯 Keyword Suggester":
        show_keyword_tool()
    elif tool_option == "🤖 AI Humanizer":
        show_humanizer_tool()

def show_analyze_tool():
    """Content Analysis Tool"""
    st.header("🔍 Content Analyzer")
    st.markdown("Get detailed insights about your content's readability, SEO score, and optimization opportunities.")
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_text = st.text_area(
            "📝 Enter your content to analyze:",
            height=300,
            placeholder="Paste your blog post, article, or any content here..."
        )
        
        if st.button("🔍 Analyze Content", type="primary", use_container_width=True):
            if user_text.strip():
                analyze_content(user_text)
            else:
                st.error("Please enter some content to analyze.")
    
    with col2:
        if st.session_state.get('analysis_results'):
            display_analysis_metrics(st.session_state.analysis_results)

def show_enhance_tool():
    """Content Enhancement Tool"""
    st.header("✨ Enhancify - Content Enhancement")
    st.markdown("Improve your content for better SEO, readability, or overall quality.")
    
    # Enhancement type selection
    enhancement_type = st.selectbox(
        "🎯 Choose enhancement type:",
        ["general", "seo", "readability"],
        format_func=lambda x: {
            "general": "🌟 General Enhancement",
            "seo": "🔍 SEO Optimization", 
            "readability": "📖 Readability Improvement"
        }[x]
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Original Content")
        user_text = st.text_area(
            "Enter content to enhance:",
            height=300,
            placeholder="Paste your content here for enhancement..."
        )
        
        if st.button("✨ Enhance Content", type="primary", use_container_width=True):
            if user_text.strip():
                enhance_content(user_text, enhancement_type)
            else:
                st.error("Please enter some content to enhance.")
    
    with col2:
        st.subheader("🚀 Enhanced Content")
        if st.session_state.get('enhanced_content'):
            enhanced = st.session_state.enhanced_content
            
            st.text_area(
                "Enhanced version:",
                value=enhanced.get('enhanced_text', ''),
                height=300,
                disabled=True
            )
            
            if enhanced.get('changes_made'):
                with st.expander("📋 Changes Made"):
                    for change in enhanced['changes_made']:
                        st.write(f"• {change}")
            
            # Download button
            if enhanced.get('enhanced_text'):
                st.download_button(
                    "📥 Download Enhanced Content",
                    enhanced['enhanced_text'],
                    file_name="enhanced_content.txt",
                    mime="text/plain"
                )
        else:
            st.info("Enhanced content will appear here after processing.")

def show_keyword_tool():
    """Keyword Suggestion Tool"""
    st.header("🎯 Keyword Suggester")
    st.markdown("Generate targeted keywords for better SEO performance.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        user_text = st.text_area(
            "📝 Enter your content or topic:",
            height=200,
            placeholder="Enter your content, topic, or niche..."
        )
        
        target_count = st.slider("🎯 Number of keywords to generate:", 5, 20, 10)
        
        if st.button("🎯 Generate Keywords", type="primary", use_container_width=True):
            if user_text.strip():
                generate_keywords(user_text, target_count)
            else:
                st.error("Please enter some content or topic.")
    
    with col2:
        if st.session_state.get('keyword_results'):
            display_keyword_results(st.session_state.keyword_results)

def show_humanizer_tool():
    """AI Humanizer Tool"""
    st.header("🤖 AI Humanizer")
    st.markdown("Transform AI-generated content into natural, human-like text.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🤖 AI-Generated Content")
        user_text = st.text_area(
            "Enter AI-generated content:",
            height=300,
            placeholder="Paste your AI-generated content here to make it more human-like..."
        )
        
        if st.button("🤖 Humanize Content", type="primary", use_container_width=True):
            if user_text.strip():
                humanize_content(user_text)
            else:
                st.error("Please enter some content to humanize.")
    
    with col2:
        st.subheader("👤 Humanized Content")
        if st.session_state.get('humanized_content'):
            humanized = st.session_state.humanized_content
            
            st.text_area(
                "Humanized version:",
                value=humanized.get('humanized_text', ''),
                height=300,
                disabled=True
            )
            
            # Human score
            if humanized.get('human_score'):
                st.metric("🧠 Human Score", f"{humanized['human_score']}/100")
            
            if humanized.get('changes_made'):
                with st.expander("🔄 Changes Made"):
                    for change in humanized['changes_made']:
                        st.write(f"• {change}")
            
            # Download button
            if humanized.get('humanized_text'):
                st.download_button(
                    "📥 Download Humanized Content",
                    humanized['humanized_text'],
                    file_name="humanized_content.txt",
                    mime="text/plain"
                )
        else:
            st.info("Humanized content will appear here after processing.")

def analyze_content(text: str):
    """Analyze content using the API"""
    with st.spinner("🔍 Analyzing your content..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/analyze",
                json={"text": text},
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json()
            st.session_state.analysis_results = results
            
            if results.get('success'):
                st.success("✅ Analysis completed successfully!")
            else:
                st.warning("⚠️ Analysis completed with limited results.")
            
            st.rerun()
            
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to the analysis server. Please ensure the backend is running.")
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")

def enhance_content(text: str, enhancement_type: str):
    """Enhance content using the API"""
    with st.spinner(f"✨ Enhancing your content for {enhancement_type}..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/enhance",
                json={"text": text, "enhancement_type": enhancement_type},
                timeout=60
            )
            response.raise_for_status()
            
            results = response.json()
            st.session_state.enhanced_content = results
            
            if results.get('success'):
                st.success("✅ Content enhanced successfully!")
            else:
                st.warning("⚠️ Enhancement completed with limited results.")
            
            st.rerun()
            
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to the enhancement server.")
        except Exception as e:
            st.error(f"❌ Enhancement failed: {str(e)}")

def generate_keywords(text: str, target_count: int):
    """Generate keywords using the API"""
    with st.spinner("🎯 Generating keywords..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/keywords",
                json={"text": text, "target_count": target_count},
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json()
            st.session_state.keyword_results = results
            
            if results.get('success'):
                st.success("✅ Keywords generated successfully!")
            else:
                st.warning("⚠️ Keywords generated with limited results.")
            
            st.rerun()
            
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to the keyword server.")
        except Exception as e:
            st.error(f"❌ Keyword generation failed: {str(e)}")

def humanize_content(text: str):
    """Humanize content using the API"""
    with st.spinner("🤖 Humanizing your content..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/humanize",
                json={"text": text},
                timeout=60
            )
            response.raise_for_status()
            
            results = response.json()
            st.session_state.humanized_content = results
            
            if results.get('success'):
                st.success("✅ Content humanized successfully!")
            else:
                st.warning("⚠️ Humanization completed with limited results.")
            
            st.rerun()
            
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to the humanization server.")
        except Exception as e:
            st.error(f"❌ Humanization failed: {str(e)}")

def display_analysis_metrics(results: Dict[str, Any]):
    """Display analysis results in sidebar"""
    st.subheader("📊 Analysis Results")
    
    # Key metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("📖 Readability", f"{results.get('readability_score', 0):.1f}/100")
        st.metric("📝 Words", results.get('word_count', 0))
    
    with col2:
        st.metric("🎯 SEO Score", f"{results.get('seo_score', 0)}/100")
        st.metric("📄 Sentences", results.get('sentence_count', 0))
    
    # Keywords found
    if results.get('keywords'):
        st.subheader("🔑 Keywords Found")
        for keyword in results['keywords'][:5]:
            st.code(keyword, language=None)
    
    # Improvements
    if results.get('improvements'):
        st.subheader("💡 Suggestions")
        for improvement in results['improvements'][:3]:
            if improvement.strip():
                st.write(f"• {improvement}")

def display_keyword_results(results: Dict[str, Any]):
    """Display keyword results"""
    st.subheader("🎯 Generated Keywords")
    
    # Primary keywords
    if results.get('primary_keywords'):
        st.write("**🏆 Primary Keywords:**")
        for keyword in results['primary_keywords']:
            st.code(keyword, language=None)
    
    # Secondary keywords
    if results.get('secondary_keywords'):
        st.write("**🥈 Secondary Keywords:**")
        for keyword in results['secondary_keywords']:
            st.code(keyword, language=None)
    
    # Long tail keywords
    if results.get('long_tail_keywords'):
        st.write("**📏 Long-tail Keywords:**")
        for keyword in results['long_tail_keywords']:
            st.code(keyword, language=None)
    
    # Export all keywords
    all_keywords = []
    for category in ['primary_keywords', 'secondary_keywords', 'long_tail_keywords', 'semantic_keywords']:
        all_keywords.extend(results.get(category, []))
    
    if all_keywords:
        keywords_text = '\n'.join(all_keywords)
        st.download_button(
            "📥 Download All Keywords",
            keywords_text,
            file_name="keywords.txt",
            mime="text/plain"
        )

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'enhanced_content' not in st.session_state:
    st.session_state.enhanced_content = None
if 'keyword_results' not in st.session_state:
    st.session_state.keyword_results = None
if 'humanized_content' not in st.session_state:
    st.session_state.humanized_content = None

if __name__ == "__main__":
    main()