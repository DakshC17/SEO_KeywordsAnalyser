# SEO Tools Suite

A comprehensive AI-powered SEO toolkit built with Streamlit (frontend) and FastAPI (backend) that provides four essential tools for content optimization and analysis.

## ✨ Features

### 🔍 Content Analyzer
- **Readability Analysis**: Get detailed readability scores using advanced algorithms
- **SEO Scoring**: Comprehensive SEO analysis with actionable insights
- **Keyword Detection**: Automatic extraction of relevant keywords from content
- **Metrics Dashboard**: Real-time display of word count, sentence count, and optimization suggestions

### ✨ Enhancify - Content Enhancement
- **SEO Optimization**: Enhance content for better search engine rankings
- **Readability Improvement**: Simplify complex sentences and improve flow
- **General Enhancement**: Overall quality improvement with better structure and tone
- **AI-Powered Suggestions**: Get specific recommendations for content improvement

### 🎯 Keyword Suggester
- **Primary Keywords**: Generate main target keywords for your content
- **Secondary Keywords**: Related keywords for broader coverage
- **Long-tail Keywords**: Specific phrases for niche targeting
- **Semantic Keywords**: Contextually related terms for better SEO
- **Bulk Export**: Download all generated keywords in text format

### 🤖 AI Humanizer
- **Natural Language Processing**: Transform AI-generated content into human-like text
- **Conversational Tone**: Add personality and natural variations
- **Human Score**: Get quantified feedback on how human-like your content sounds
- **Change Tracking**: See exactly what modifications were made

## 🛠️ Technology Stack

### Frontend (Streamlit)
- Modern, responsive UI with tool selection
- Real-time processing indicators
- Side-by-side content comparison
- Export functionality for all tools
- Session state management

### Backend (FastAPI)
- RESTful API architecture
- Groq integration with Llama 3 model
- Async processing for better performance
- Comprehensive error handling
- Health check endpoints

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd seo-tools-suite
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv myvenv
   source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the `backend/` directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

   Get your Groq API key from [console.groq.com](https://console.groq.com)

## 🚀 Usage

1. **Start the FastAPI backend:**
   ```bash
   cd backend
   python main.py
   ```
   The API will be available at `http://localhost:8000`

2. **Start the Streamlit frontend:**
   ```bash
   cd frontend
   streamlit run streamlit_app.py
   ```
   The web app will open at `http://localhost:8501`

3. **Using the Application:**
   - Select your desired tool from the sidebar
   - Enter your content in the input area
   - Process your content with AI-powered analysis
   - Export or download the results

## 🔧 API Endpoints

### POST /analyze
Analyzes content for readability, SEO metrics, and suggestions.

**Request:**
```json
{
  "text": "Your content here..."
}
```

**Response:**
```json
{
  "readability_score": 75.5,
  "word_count": 150,
  "sentence_count": 8,
  "keywords": ["keyword1", "keyword2"],
  "seo_score": 80,
  "improvements": ["suggestion1", "suggestion2"],
  "meta_description": "Generated meta description",
  "success": true
}
```

### POST /enhance
Enhances content for SEO, readability, or general improvement.

**Request:**
```json
{
  "text": "Original content...",
  "enhancement_type": "seo"
}
```

**Response:**
```json
{
  "enhanced_text": "Improved content...",
  "changes_made": ["change1", "change2"],
  "improvements": ["improvement1", "improvement2"],
  "success": true
}
```

### POST /keywords
Generates keyword suggestions categorized by type.

**Request:**
```json
{
  "text": "Content for keyword analysis...",
  "target_count": 10
}
```

**Response:**
```json
{
  "primary_keywords": ["main keyword 1", "main keyword 2"],
  "secondary_keywords": ["related keyword 1", "related keyword 2"],
  "long_tail_keywords": ["long tail phrase 1"],
  "semantic_keywords": ["semantic keyword 1"],
  "success": true
}
```

### POST /humanize
Makes AI-generated content more human-like.

**Request:**
```json
{
  "text": "AI-generated content..."
}
```

**Response:**
```json
{
  "humanized_text": "More natural sounding content...",
  "changes_made": ["change1", "change2"],
  "human_score": 85,
  "success": true
}
```

### GET /health
Health check endpoint to verify API status.

**Response:**
```json
{
  "status": "healthy",
  "ai_service_available": true,
  "version": "2.0.0"
}
```

## 📁 Project Structure

```
seo-tools-suite/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── ai_service.py        # Groq AI integration
│   └── .env                 # Environment variables
├── frontend/
│   └── streamlit_app.py     # Streamlit web application
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🎯 Tool Descriptions

### Content Analyzer
Perfect for bloggers, content creators, and marketers who need detailed insights about their content's SEO performance and readability. Get actionable suggestions for improvement.

### Enhancify
Choose from three enhancement modes:
- **SEO**: Optimize for search engines with keyword density improvements
- **Readability**: Simplify complex language for better user engagement
- **General**: Overall quality enhancement for professional content

### Keyword Suggester
Generate comprehensive keyword lists for your content strategy. Get primary targets, secondary options, long-tail opportunities, and semantic variations.

### AI Humanizer
Essential for anyone using AI writing tools. Transform robotic AI-generated content into natural, engaging text that resonates with human readers.

## ⚙️ Configuration

### AI Model Settings
The application uses Groq's Llama 3 model. You can modify the model in `ai_service.py`:

```python
self.model = "llama3-8b-8192"  # Fast, good quality
# or
self.model = "llama3-70b-8192"  # Slower, better quality
```

### Custom Enhancements
Each tool can be customized by modifying the prompts in `ai_service.py` to match your specific use case or industry requirements.

## 🐛 Troubleshooting

### Common Issues

1. **Backend Connection Error:**
   - Ensure FastAPI server is running on port 8000
   - Check if the backend URL in frontend is correct
   - Verify no firewall blocking

2. **Groq API Issues:**
   - Verify API key in `.env` file is correct
   - Check API quota and rate limits
   - Ensure internet connectivity

3. **Streamlit Issues:**
   - Try a different port: `streamlit run streamlit_app.py --server.port 8502`
   - Clear Streamlit cache: `streamlit cache clear`
   - Check Python version compatibility

4. **Model Errors:**
   - Verify the model name is correct and supported
   - Check Groq service status
   - Try switching to a different model

## 📊 Performance Tips

- **Caching**: API responses are cached for 5 minutes to improve performance
- **Timeouts**: Adjust timeout values in the frontend for slower internet connections
- **Batch Processing**: For multiple texts, process them one at a time to avoid rate limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-tool`
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Adding New Tools
To add a new tool:
1. Add the endpoint in `backend/main.py`
2. Implement the AI service method in `ai_service.py`
3. Create the UI function in `streamlit_app.py`
4. Add the tool option to the sidebar selector

## 📝 Dependencies

```txt
streamlit>=1.28.0
fastapi>=0.104.0
uvicorn>=0.24.0
requests>=2.31.0
python-dotenv>=1.0.0
pydantic>=2.4.0
groq>=0.4.1
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section above
- Review the API documentation
- Test with the health endpoint: `http://localhost:8000/health`
- Open an issue on GitHub

## 🚀 Future Enhancements

- [ ] Bulk processing capabilities
- [ ] Content templates and presets
- [ ] Integration with popular CMS platforms
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] API rate limiting and user management