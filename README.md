A production-ready web application that generates AI-powered research briefs from multiple URLs using FastAPI, SQLite (Dev) / PostgreSQL (Prod), and Groq/Llama-3.

## 🎯 Features

- **URL Submission**: Submit 1-10 URLs for analysis
- **AI-Powered Analysis**: Uses OpenAI to generate structured research briefs
- **Comprehensive Output**: 
  - Executive summary
  - Key points with source attribution
  - Conflicting claims across sources
  - Verification checklist
- **Recent Briefs**: View last 5 research briefs
- **Health Monitoring**: `/status` endpoint for system health checks
- **Production Ready**: Fully compatible with Render Web Services

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI
- **Database**: PostgreSQL (external, managed)
- **ORM**: SQLAlchemy
- **Templates**: Jinja2
- **Styling**: TailwindCSS (CDN)
- **HTTP Client**: httpx
- **Content Extraction**: readability-lxml
- **AI**: Groq API (OpenAI-compatible) with Llama-3.3-70b-versatile
- **Specialized Fetching**: Uses Wikipedia REST API for Wikipedia links to bypass blocks
- **Environment**: python-dotenv

## 📋 Requirements

- Python 3.11+
- PostgreSQL database
- OpenAI API key

## 🚀 Local Development Setup

### 1. Clone and Setup Environment

```bash
# Navigate to project directory
cd vibu

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/research_brief_db
OPENAI_API_KEY=gsk_your_groq_api_key_here
OPENAI_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.3-70b-versatile
ENVIRONMENT=development
PORT=8000
```

### 3. Setup PostgreSQL Database

```bash
# Create database
createdb research_brief_db

# Or using psql
psql -U postgres
CREATE DATABASE research_brief_db;
```

### 4. Run the Application

```bash
# Using uvicorn directly
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Or using Python
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The application will be available at `http://127.0.0.1:8000`

### 5. Test the Application

- **Home Page**: `http://127.0.0.1:8000/`
- **Health Check**: `http://127.0.0.1:8000/status`

## 🌐 Deployment to Render

### Prerequisites

1. Create a [Render](https://render.com) account
2. Create a PostgreSQL database on Render
3. Have your OpenAI API key ready

### Step-by-Step Deployment

#### 1. Create PostgreSQL Database

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `research-brief-db`
   - **Database**: `research_brief_db`
   - **User**: (auto-generated)
   - **Region**: Choose closest to you
   - **Plan**: Free or paid
4. Click "Create Database"
5. Copy the **Internal Database URL** (starts with `postgresql://`)

#### 2. Create Web Service

1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Connect your Git repository
4. Configure:
   - **Name**: `research-brief-app`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`

#### 3. Set Environment Variables

In the Render dashboard, add these environment variables:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | (Paste Internal Database URL from step 1) |
| `OPENAI_API_KEY` | (Your OpenAI API key) |
| `ENVIRONMENT` | `production` |
| `PORT` | `10000` |
| `PYTHON_VERSION` | `3.11.0` |

#### 4. Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Install dependencies
   - Initialize database tables
   - Start the application
3. Wait for deployment to complete (2-5 minutes)
4. Access your app at the provided URL (e.g., `https://research-brief-app.onrender.com`)

### Verify Deployment

1. Visit your app URL
2. Check health status: `https://your-app.onrender.com/status`
3. Should return:
   ```json
   {
     "backend": "ok",
     "database": "ok",
     "llm": "ok"
   }
   ```

## 📁 Project Structure

```
vibu/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py          # Main routes
│   │   └── health.py        # Health check routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── article_extractor.py  # URL fetching & extraction
│   │   └── llm_service.py        # OpenAI integration
│   └── templates/
│       ├── home.html        # Home page
│       └── brief.html       # Results page
├── venv/                    # Virtual environment
├── .env                     # Environment variables (not in git)
├── .env.example             # Environment template
├── .gitignore
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── AI_NOTES.md             # AI development notes
├── PROMPTS_USED.md         # Prompts documentation
└── ABOUTME.md              # Developer information
```

## 🔍 API Endpoints

### Web Pages

- `GET /` - Home page with URL submission form
- `GET /brief/{brief_id}` - View research brief results

### API Endpoints

- `POST /submit` - Submit URLs for processing
  - Body: `{"urls": ["url1", "url2", ...]}`
  - Returns: Brief ID and status
- `GET /api/brief/{brief_id}` - Get brief data as JSON
- `GET /status` - Health check endpoint

## ✅ What's Implemented

- ✅ URL submission with validation (1-10 URLs)
- ✅ Background processing with status tracking
- ✅ Article extraction using readability-lxml
- ✅ OpenAI integration with structured JSON output
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Jinja2 templates with TailwindCSS
- ✅ Last 5 briefs display on homepage
- ✅ Health check endpoint with real checks
- ✅ Proper error handling and logging
- ✅ Render-compatible deployment configuration
- ✅ Type hints throughout codebase
- ✅ Clean separation of concerns (routes/services/models)

## ❌ What's Not Implemented

- ❌ User authentication/authorization
- ❌ Brief editing or deletion
- ❌ Export to PDF/Word
- ❌ Email notifications
- ❌ Rate limiting
- ❌ Caching layer
- ❌ Webhook support
- ❌ Multi-language support

## 🔧 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `OPENAI_API_KEY` | OpenAI API key | Yes | - |
| `ENVIRONMENT` | Environment (development/production) | No | development |
| `PORT` | Server port | No | 8000 |

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Test database connection
psql $DATABASE_URL

# Check if tables exist
psql $DATABASE_URL -c "\dt"
```

### OpenAI API Issues

- Verify API key is valid
- Check OpenAI account has credits
- Review logs for specific error messages

### Port Already in Use

```bash
# Windows - Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## 📝 License

This project is for educational and assignment purposes.

## 👤 Author

See [ABOUTME.md](ABOUTME.md) for developer information.
