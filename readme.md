# SEO Analyzer Web App

A comprehensive SEO content analyzer built with Streamlit (frontend) and FastAPI (backend) that helps optimize your content for better search engine visibility.

## Features

### Frontend (Streamlit)
- 📝 Large text area for content input (blogs, tweets, captions)
- 🔍 Real-time SEO analysis with readability scoring
- 🎯 Keyword recommendations with intelligent insertion
- ✨ Visual highlighting of inserted keywords
- 📊 Comprehensive analysis sidebar with metrics
- 🔄 Reset and export functionality
- 📱 Clean, responsive user interface

### Backend (FastAPI)
- 🚀 Fast API endpoints for text analysis
- 🔑 Razor API integration for keyword suggestions
- 🧠 Intelligent keyword insertion algorithm
- 📈 Readability score calculation
- 🛡️ Robust error handling and validation
- 🔒 Environment-based configuration

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd seo-analyzer
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
   ```
   RAZOR_API_KEY=your_razor_api_key_here
   ```

## Usage

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
   - Enter your content in the text area
   - Click "Analyze Content" to get SEO insights
   - Review recommended keywords and readability score
   - Click "Insert" buttons to add keywords intelligently
   - Export your optimized content

## API Endpoints

### POST /analyze
Analyzes text content and returns SEO metrics.

**Request:**
```json
{
  "text": "Your content here..."
}
```

**Response:**
```json
{
  "readability_score": 75.2,
  "keywords": [
    {
      "keyword": "example",
      "weight": 0.9,
      "relevance": 0.8,
      "difficulty": 0.3
    }
  ],
  "word_count": 150
}
```

### POST /insert_keyword
Intelligently inserts a keyword into existing text.

**Request:**
```json
{
  "text": "Original text...",
  "keyword": "SEO"
}
```

**Response:**
```json
{
  "modified_text": "Original text with SEO keyword inserted..."
}
```

## Project Structure

```
seo-analyzer/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── keyword_utils.py     # Keyword insertion logic
│   └── .env                 # Environment variables
├── frontend/
│   └── streamlit_app.py     # Streamlit web application
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Features in Detail

### Intelligent Keyword Insertion
- Avoids duplicating existing keywords
- Maintains sentence structure and readability
- Uses contextual placement strategies
- Provides natural language integration

### Readability Analysis
- Implements Flesch Reading Ease formula
- Provides actionable readability insights
- Color-coded difficulty indicators

### SEO Scoring
- Combines multiple factors for overall SEO score
- Real-time metrics updating
- Visual progress indicators

### Caching & Performance
- Streamlit caching for API calls
- Optimized for responsive user experience
- Efficient text processing algorithms

## Customization

### Adding New Metrics
1. Extend the analysis endpoint in `backend/main.py`
2. Update the frontend display in `streamlit_app.py`
3. Add corresponding UI elements

### Keyword Insertion Strategies
Modify `keyword_utils.py` to implement custom insertion logic:
- Semantic positioning
- Density-based placement
- Context-aware insertion

## Troubleshooting

### Common Issues

1. **Backend Connection Error:**
   - Ensure FastAPI server is running on port 8000
   - Check firewall settings

2. **Razor API Issues:**
   - Verify API key in `.env` file
   - Check API quota and limits
   - Review network connectivity

3. **Streamlit Port Conflicts:**
   - Use `streamlit run streamlit_app.py --server.port 8502` for different port

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation
- Open an issue on GitHub