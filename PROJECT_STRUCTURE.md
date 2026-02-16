# Project Structure

## Complete Folder Structure

```
vibu/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application entry point
│   ├── database.py              # Database configuration and session management
│   ├── models.py                # SQLAlchemy database models
│   ├── schemas.py               # Pydantic validation schemas
│   │
│   ├── routes/                  # API route handlers
│   │   ├── __init__.py
│   │   ├── main.py             # Main routes (home, submit, view brief)
│   │   └── health.py           # Health check endpoint
│   │
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── article_extractor.py  # URL fetching and content extraction
│   │   └── llm_service.py        # OpenAI integration
│   │
│   └── templates/              # Jinja2 HTML templates
│       ├── home.html           # Home page with URL submission
│       └── brief.html          # Research brief results page
│
├── venv/                       # Virtual environment (not in git)
│
├── .env                        # Environment variables (not in git)
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
│
├── README.md                   # Main documentation
├── QUICKSTART.md              # Quick start guide
├── AI_NOTES.md                # AI development notes
├── PROMPTS_USED.md            # Prompts documentation
├── ABOUTME.md                 # Developer information
└── PROJECT_STRUCTURE.md       # This file
```

## File Descriptions

### Core Application Files

#### `app/main.py`
- FastAPI application initialization
- CORS middleware configuration
- Router registration
- Startup/shutdown event handlers
- Logging configuration

**Key Features**:
- Binds to `0.0.0.0` for Render compatibility
- Uses PORT environment variable
- Initializes database on startup

#### `app/database.py`
- SQLAlchemy engine creation
- Session factory configuration
- Database dependency injection
- Table initialization function

**Key Features**:
- Connection pooling with `pool_pre_ping`
- Generator-based session management
- Automatic cleanup

#### `app/models.py`
- `ResearchBrief` SQLAlchemy model
- Database schema definition

**Fields**:
- `id`: UUID primary key
- `created_at`: Timestamp with timezone
- `raw_urls`: JSON array of submitted URLs
- `result`: JSON object with research brief
- `status`: String (processing/completed/failed)
- `error_message`: Text field for errors

#### `app/schemas.py`
- Pydantic models for validation
- Request/response schemas

**Schemas**:
- `URLSubmission`: Validates 1-10 URLs
- `ResearchBriefResult`: Structured brief format
- `ResearchBriefResponse`: API response format
- `HealthCheckResponse`: Health status format

### Routes

#### `app/routes/main.py`
Main application routes:

- `GET /` - Home page with submission form
- `POST /submit` - Submit URLs for processing
- `GET /brief/{brief_id}` - View research brief (HTML)
- `GET /api/brief/{brief_id}` - Get brief data (JSON)

**Background Processing**:
- Creates database record with status="processing"
- Processes URLs asynchronously
- Updates status to completed/failed

#### `app/routes/health.py`
Health monitoring:

- `GET /status` - System health check

**Checks**:
- Backend: Always "ok" if reachable
- Database: Real connection test
- LLM: API key validation

### Services

#### `app/services/article_extractor.py`
Article extraction service:

**Methods**:
- `fetch_and_extract(url)`: Fetch single URL
- `fetch_multiple(urls)`: Fetch multiple URLs

**Features**:
- Uses httpx for async HTTP requests
- readability-lxml for content extraction
- HTML tag removal and cleaning
- Content length limiting (5000 chars)
- Error handling per URL

#### `app/services/llm_service.py`
OpenAI integration service:

**Methods**:
- `generate_brief(articles)`: Generate research brief
- `validate_api_key()`: Validate OpenAI key

**Features**:
- Structured JSON output enforcement
- Response format validation
- Comprehensive prompt building
- Error handling and logging

### Templates

#### `app/templates/home.html`
Home page features:

- URL submission form (textarea)
- Real-time URL count
- Client-side validation
- Loading states
- Recent briefs display (last 5)
- Status indicators
- Responsive design with TailwindCSS

#### `app/templates/brief.html`
Results page with three states:

**Processing State**:
- Loading spinner
- Auto-refresh every 3 seconds

**Failed State**:
- Error message display
- Submitted URLs list

**Completed State**:
- Summary section
- Key points with sources
- Conflicting claims
- Verification checklist
- Sources list

### Configuration Files

#### `requirements.txt`
Python dependencies with pinned versions:
- FastAPI 0.115.0
- Uvicorn 0.32.0
- SQLAlchemy 2.0.36
- PostgreSQL driver
- OpenAI SDK
- And more...

#### `.env.example`
Environment variable template:
```env
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
ENVIRONMENT=development
PORT=8000
```

#### `.gitignore`
Excludes from version control:
- Virtual environment
- `.env` file
- Python cache files
- IDE files
- OS files

### Documentation Files

#### `README.md`
- Project overview
- Features list
- Tech stack
- Local setup instructions
- Render deployment guide
- API documentation
- Troubleshooting

#### `QUICKSTART.md`
- Step-by-step setup
- Testing procedures
- Troubleshooting guide
- Success checklist

#### `AI_NOTES.md`
- AI tools used
- Manual verification
- OpenAI selection rationale
- Development workflow
- Lessons learned

#### `PROMPTS_USED.md`
- All prompts used
- Prompt engineering notes
- Best practices

#### `ABOUTME.md`
- Developer information
- Resume placeholder

## Data Flow

### 1. URL Submission Flow

```
User (Browser)
    ↓
GET / → home.html
    ↓
User submits URLs
    ↓
POST /submit → main.py
    ↓
Create ResearchBrief (status=processing)
    ↓
Return brief_id to user
    ↓
Redirect to /brief/{brief_id}
```

### 2. Background Processing Flow

```
Background Task Started
    ↓
article_extractor.fetch_multiple(urls)
    ↓
For each URL:
    - Fetch with httpx
    - Extract with readability-lxml
    - Clean HTML
    ↓
llm_service.generate_brief(articles)
    ↓
OpenAI API call
    ↓
Parse JSON response
    ↓
Update ResearchBrief:
    - result = JSON data
    - status = completed/failed
```

### 3. Results Display Flow

```
GET /brief/{brief_id}
    ↓
Query database for brief
    ↓
If status == processing:
    - Show spinner
    - Auto-refresh
    ↓
If status == failed:
    - Show error
    ↓
If status == completed:
    - Display full research brief
```

## Database Schema

### `research_briefs` Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(36) | PRIMARY KEY | UUID |
| created_at | TIMESTAMP | NOT NULL | Creation time |
| raw_urls | JSON | NOT NULL | Submitted URLs |
| result | JSON | NULLABLE | Research brief |
| status | VARCHAR(20) | NOT NULL | processing/completed/failed |
| error_message | TEXT | NULLABLE | Error details |

### Indexes

- Primary key on `id`
- Implicit index on `created_at` for sorting recent briefs

## API Response Formats

### Health Check Response
```json
{
  "backend": "ok",
  "database": "ok",
  "llm": "ok"
}
```

### Research Brief Response
```json
{
  "id": "uuid-here",
  "created_at": "2026-02-17T00:00:00Z",
  "raw_urls": ["url1", "url2"],
  "result": {
    "summary": "...",
    "key_points": [...],
    "conflicting_claims": [...],
    "verification_checklist": [...]
  },
  "status": "completed",
  "error_message": null
}
```

## Deployment Architecture

### Local Development
```
Browser → localhost:8000 → FastAPI → PostgreSQL (local)
                                   → OpenAI API
```

### Render Production
```
Browser → render.com → Web Service → PostgreSQL (Render)
                                   → OpenAI API
```

## Key Design Decisions

### 1. No Docker
- Render Web Services supports Python natively
- Simpler deployment without Docker
- Faster builds

### 2. Background Processing
- Prevents request timeout
- Better user experience
- Allows long-running LLM calls

### 3. Structured JSON Output
- Enforces consistent format
- Eliminates parsing errors
- Easier to validate

### 4. Separate Services Layer
- Clean separation of concerns
- Easier testing
- Better maintainability

### 5. TailwindCSS via CDN
- No build step required
- Faster development
- Simpler deployment

## Security Considerations

### Implemented
- ✅ Environment variables for secrets
- ✅ No hardcoded credentials
- ✅ `.env` in `.gitignore`
- ✅ Input validation with Pydantic
- ✅ SQL injection prevention (SQLAlchemy ORM)

### Not Implemented (Future)
- ❌ Rate limiting
- ❌ User authentication
- ❌ CSRF protection
- ❌ API key rotation
- ❌ Request signing

## Performance Considerations

### Current Implementation
- Async HTTP requests with httpx
- Connection pooling for database
- Background task processing
- Content length limiting

### Future Optimizations
- Parallel article fetching
- Response caching
- Database query optimization
- CDN for static assets

## Monitoring and Logging

### Current Logging
- Application startup/shutdown
- Database initialization
- Article fetching
- LLM generation
- Error tracking

### Log Levels
- `INFO`: Normal operations
- `WARNING`: Potential issues
- `ERROR`: Failures

### Future Monitoring
- Application performance monitoring (APM)
- Error tracking (Sentry)
- Usage analytics
- Cost tracking (OpenAI API)

## Testing Strategy

### Manual Testing
- URL submission with valid/invalid URLs
- Background processing
- Error handling
- Health checks
- UI responsiveness

### Future Automated Testing
- Unit tests for services
- Integration tests for routes
- End-to-end tests
- Load testing

## Maintenance

### Regular Tasks
- Monitor OpenAI API costs
- Check database size
- Review error logs
- Update dependencies

### Backup Strategy
- Database backups (Render automatic)
- Environment variable documentation
- Code in version control
