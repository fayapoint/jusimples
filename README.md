# JuSimples - Legal AI Assistant Platform

## 🎯 Vision
JuSimples is a revolutionary legal AI platform designed to democratize access to legal information in Brazil. Using advanced Retrieval-Augmented Generation (RAG) architecture, we provide accurate, contextual legal guidance to both ordinary citizens and legal professionals.

## ✨ Features

### For Citizens
- **Simple Legal Consultation**: Ask legal questions in plain Portuguese
- **Document Analysis**: Upload and analyze legal documents
- **Rights Information**: Learn about your fundamental rights
- **Process Guidance**: Step-by-step guidance for legal procedures

### For Legal Professionals
- **Advanced Legal Research**: Semantic search across Brazilian legal corpus
- **Case Law Analysis**: AI-powered analysis of jurisprudence
- **Document Generation**: Automated legal document templates
- **Compliance Checking**: LGPD and regulatory compliance tools

## 🛠 Technology Stack

### Frontend
- **React 19**: Modern UI framework with latest features
- **Framer Motion**: Smooth animations and micro-interactions
- **Lucide React**: Beautiful icon library
- **Axios**: API communication
- **CSS Variables**: Dark theme with glassmorphism effects

### Backend (RAG Architecture)
- **Python Flask**: RESTful API framework
- **LangChain**: LLM orchestration and RAG pipeline
- **ChromaDB**: Vector database for semantic search
- **OpenAI GPT-4**: Language model for AI responses
- **Sentence Transformers**: Text embeddings
- **BeautifulSoup**: Legal document scraping
- **LexML Integration**: Brazilian legal data collection

### Infrastructure
- **Docker**: Containerization
- **PostgreSQL**: Primary database (planned)
- **Redis**: Caching layer (planned)
- **Nginx**: Reverse proxy (planned)
- **Cloud Deployment**: AWS/GCP ready

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- Python 3.8+
- Git

### Automated Setup

1. **Clone the repository**
```bash
git clone https://github.com/fayapoint/jusimples.git
cd jusimples
```

2. **Run setup script**
```bash
python setup.py
```

3. **Configure API keys**
```bash
# Edit backend/.env with your API keys
# At minimum, set OPENAI_API_KEY for AI functionality
```

4. **Start the application**
```bash
# Terminal 1 - Backend
cd backend
python start_backend.py

# Terminal 2 - Frontend
cd frontend
npm start
```

5. **Access the Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

### Manual Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac
pip install -r requirements.txt
cp .env.example .env
# Configure your API keys in .env
python start_backend.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 📊 Project Structure

```
jusimples/
├── frontend/                    # React application
│   ├── src/
│   │   ├── App.js              # Main app component
│   │   ├── App.css             # Sophisticated dark theme
│   │   └── index.js            # Entry point
│   ├── public/                 # Static assets
│   └── package.json            # Dependencies
├── backend/                    # Python Flask API with RAG
│   ├── app.py                  # Main Flask app with RAG system
│   ├── lexml_scraper.py        # Legal document scraper
│   ├── data_collector.py       # Data collection service
│   ├── start_backend.py        # Backend startup script
│   ├── test_rag_system.py      # RAG system tests
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example           # Environment configuration
│   └── chroma_db/             # Vector database storage
├── setup.py                   # Automated setup script
└── README.md                  # This file
```
- [ ] **Phase 4**: Advanced LLM integration (GPT-4/Claude)
- [ ] **Phase 5**: User authentication and management
- [ ] **Phase 6**: LGPD compliance and security measures

## 📊 Project Vision

JuSimples aims to democratize access to legal information in Brazil by:

- **Serving Two Audiences**: Citizens seeking basic legal guidance and lawyers needing advanced research tools
- **RAG Architecture**: Retrieval-Augmented Generation for accurate, source-backed responses
- **Brazilian Legal Focus**: Comprehensive coverage of federal laws with plans for state/municipal expansion
- **Premium UX**: Extraordinary user experience that builds trust and engagement

## 💰 Investment & Timeline

- **MVP Development**: 4-6 months
- **Estimated Budget**: R$ 85,000 - R$ 270,000
- **Technology Stack**: Python, React, Vector DB, LLM APIs
- **Compliance**: LGPD-ready with enterprise security

## 🤝 Contributing

This project is currently in active development. Contributions will be welcomed once the MVP is complete.

## 📄 License

This project is proprietary software. All rights reserved.

## 📞 Contact

For more information about JuSimples, please contact the development team.

---

**JuSimples** - Democratizing access to justice through AI innovation.
