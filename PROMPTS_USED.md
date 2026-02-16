# Prompts Used for Project Development

This document contains the prompts used to build this Research Brief application. **No API keys or sensitive information are included.**

## Initial Project Setup Prompt

```
You are a senior full-stack Python engineer.

We are building a production-ready web app for a technical assignment.

Project Name: Research Brief from Links

IMPORTANT:
This must match the assignment requirements EXACTLY.
The app must be fully compatible with Render Web Services (Python).
Do not use Docker.
Do not use React.
Keep it simple and deployable.

TECH STACK:
- Python 3.11
- FastAPI
- PostgreSQL (external, managed)
- SQLAlchemy ORM
- Jinja2 templates
- TailwindCSS via CDN
- httpx for fetching URLs
- readability-lxml for article extraction
- OpenAI API (structured JSON output)
- python-dotenv
- logging module

[Full requirements provided...]
```

## Database Model Design Prompt

```
Create a SQLAlchemy model for ResearchBrief with:
- UUID primary key
- Timestamp with timezone
- JSON fields for raw_urls and result
- Status field (processing/completed/failed)
- Error message field
- Proper type hints
- Clean __repr__ method
```

## OpenAI Integration Prompt

```
Create an LLM service that:
1. Takes extracted article content
2. Builds a comprehensive prompt
3. Uses OpenAI's structured JSON output
4. Enforces exact JSON format:
   {
     "summary": "",
     "key_points": [...],
     "conflicting_claims": [...],
     "verification_checklist": [...]
   }
5. Validates the response structure
6. Handles errors gracefully
7. Includes API key validation method
```

## Article Extraction Prompt

```
Create an article extraction service using:
- httpx for async HTTP requests
- readability-lxml for content extraction
- Proper HTML cleaning
- Error handling for failed fetches
- Support for multiple URLs
- Content length limiting
- Comprehensive logging
```

## Frontend Template Prompts

### Home Page
```
Create a beautiful home page with:
- TailwindCSS styling
- URL submission form (textarea for 1-10 URLs)
- Real-time URL count display
- Form validation
- Error message display
- Loading state with spinner
- Display of last 5 research briefs
- Status indicators (completed/processing/failed)
- Responsive design
- Modern, clean aesthetic
```

### Results Page
```
Create a results page that handles three states:
1. Processing - show spinner and auto-refresh
2. Failed - show error message and submitted URLs
3. Completed - show:
   - Summary section
   - Key points with source attribution
   - Conflicting claims (if any)
   - Verification checklist
   - Sources list
   
Use TailwindCSS for styling
Make it visually appealing and easy to read
```

## Health Check Endpoint Prompt

```
Create a /status endpoint that returns:
{
  "backend": "ok",
  "database": "ok" or "error",
  "llm": "ok" or "error"
}

Requirements:
- Perform REAL database connection check
- Perform lightweight OpenAI API key validation
- Don't do full LLM generation (too expensive)
- Log all checks
- Return proper status codes
```

## Background Processing Prompt

```
Implement background task processing for research briefs:
1. Create database record with status="processing"
2. Return immediately to user
3. Process in background:
   - Fetch and extract articles
   - Generate research brief with LLM
   - Update database with result
   - Set status="completed" or "failed"
4. Handle database sessions properly in background tasks
5. Comprehensive error handling
```

## Deployment Configuration Prompts

### Render Compatibility
```
Ensure the application is Render-compatible:
- Bind to 0.0.0.0
- Use PORT environment variable with fallback
- Start command: uvicorn app.main:app --host 0.0.0.0 --port 10000
- No Docker
- Works with external PostgreSQL
- Proper environment variable handling
```

### Requirements File
```
Create requirements.txt with pinned versions for:
- FastAPI
- Uvicorn with standard extras
- SQLAlchemy
- psycopg2-binary
- python-dotenv
- Jinja2
- httpx
- readability-lxml
- OpenAI
- Pydantic
- Pydantic-settings
```

## Documentation Prompts

### README
```
Create a comprehensive README with:
1. Project overview and features
2. Tech stack
3. Local development setup (step-by-step)
4. Render deployment guide (detailed)
5. Project structure
6. API endpoints documentation
7. What's implemented vs not implemented
8. Environment variables table
9. Troubleshooting section
```

### AI Notes
```
Document:
1. What AI tools were used
2. What was manually verified
3. Why OpenAI was chosen (technical reasons)
4. Alternatives considered
5. Development workflow
6. Lessons learned
7. Code quality metrics
8. Future improvements
```

## Validation and Testing Prompts

### URL Validation
```
Create Pydantic schema with:
- URL list validation (1-10 URLs)
- Regex pattern for valid URLs
- Support for http/https
- Support for domains, localhost, IPs
- Optional ports
- Proper error messages
- Strip whitespace
```

### Error Handling
```
Implement comprehensive error handling:
- Try/except blocks for all external calls
- Proper logging (not print statements)
- User-friendly error messages
- Database rollback on errors
- Status updates on failures
- Error message storage in database
```

## Code Quality Prompts

```
Ensure code quality:
- Type hints on all functions
- Docstrings for classes and functions
- Clean separation: routes/services/models
- Dependency injection for database
- No hardcoded secrets
- Logging instead of print
- No unused imports
- Consistent naming conventions
- Production-ready structure
```

## Styling and UX Prompts

```
Create modern, professional UI:
- Use TailwindCSS via CDN
- Gradient backgrounds
- Card-based layouts
- Smooth transitions
- Loading spinners
- Status indicators with colors
- Responsive design
- Clear typography
- Proper spacing
- Accessible design
```

## Notes on Prompt Engineering

### Effective Strategies Used

1. **Be Specific**: Detailed requirements prevent ambiguity
2. **Provide Context**: Explain the "why" behind requirements
3. **List Constraints**: Clearly state what NOT to do
4. **Request Structure**: Ask for specific file organization
5. **Demand Quality**: Explicitly request type hints, error handling, etc.
6. **Iterative Refinement**: Start broad, then add specific details

### Common Pitfalls Avoided

1. ❌ Vague requirements → ✅ Specific, measurable criteria
2. ❌ Assuming knowledge → ✅ Explicit tech stack and versions
3. ❌ Missing edge cases → ✅ Comprehensive error scenarios
4. ❌ Unclear success criteria → ✅ Defined "what's implemented"

### Lessons for Future Prompts

1. **Always specify deployment target** (Render, AWS, etc.)
2. **Include version numbers** for dependencies
3. **Request documentation** alongside code
4. **Specify code quality requirements** upfront
5. **Ask for error handling** explicitly
6. **Request type hints and docstrings** by default

## Conclusion

These prompts were designed to:
- Minimize ambiguity
- Ensure production-ready code
- Match assignment requirements exactly
- Create maintainable, well-documented code
- Enable successful deployment to Render

The iterative nature of AI-assisted development means these prompts were refined based on initial outputs and testing results.
