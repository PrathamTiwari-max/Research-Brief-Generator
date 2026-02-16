# Quick Start Guide

## Prerequisites Check

Before running the application, ensure you have:

- ✅ Python 3.11+ installed
- ✅ PostgreSQL installed and running
- ✅ OpenAI API key
- ✅ Virtual environment activated

## Step-by-Step Setup

### 1. Activate Virtual Environment

```powershell
# Windows PowerShell
.\venv\Scripts\activate

# You should see (venv) in your prompt
```

### 2. Install Dependencies

```powershell
# Already done if you see this file!
pip install -r requirements.txt
```

### 3. Setup PostgreSQL Database

#### Option A: Using psql command line

```powershell
# Create database
psql -U postgres -c "CREATE DATABASE research_brief_db;"

# Verify
psql -U postgres -c "\l" | findstr research_brief_db
```

#### Option B: Using pgAdmin

1. Open pgAdmin
2. Right-click on "Databases"
3. Select "Create" → "Database"
4. Name: `research_brief_db`
5. Click "Save"

### 4. Configure Environment Variables

Edit the `.env` file with your actual credentials:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/research_brief_db
OPENAI_API_KEY=sk-YOUR_ACTUAL_OPENAI_KEY
ENVIRONMENT=development
PORT=8000
```

**Important**: Replace:
- `YOUR_PASSWORD` with your PostgreSQL password
- `sk-YOUR_ACTUAL_OPENAI_KEY` with your real OpenAI API key

### 5. Test Database Connection

```powershell
# Test connection
psql postgresql://postgres:YOUR_PASSWORD@localhost:5432/research_brief_db -c "SELECT 1;"

# Should output: 1
```

### 6. Run the Application

```powershell
# Start the server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Or using Python module
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 7. Verify Application is Running

Open your browser and visit:

- **Home Page**: http://127.0.0.1:8000/
- **Health Check**: http://127.0.0.1:8000/status

Expected health check response:
```json
{
  "backend": "ok",
  "database": "ok",
  "llm": "ok"
}
```

## Testing the Application

### Test 1: Submit URLs

1. Go to http://127.0.0.1:8000/
2. Paste these test URLs (one per line):

```
https://en.wikipedia.org/wiki/Artificial_intelligence
https://en.wikipedia.org/wiki/Machine_learning
https://en.wikipedia.org/wiki/Deep_learning
```

3. Click "Generate Research Brief"
4. Wait 30-60 seconds for processing
5. View the generated research brief

### Test 2: Check Recent Briefs

1. Go back to home page
2. You should see your brief in "Recent Research Briefs"
3. Click on it to view again

### Test 3: Error Handling

Try submitting invalid URLs to test error handling:
```
not-a-valid-url
http://this-domain-definitely-does-not-exist-12345.com
```

## Troubleshooting

### Issue: Database Connection Failed

**Error**: `database connection error`

**Solution**:
1. Verify PostgreSQL is running:
   ```powershell
   Get-Service postgresql*
   ```
2. Check DATABASE_URL in `.env` file
3. Test connection manually:
   ```powershell
   psql $env:DATABASE_URL -c "SELECT 1;"
   ```

### Issue: OpenAI API Error

**Error**: `llm: error` in health check

**Solution**:
1. Verify API key is correct in `.env`
2. Check OpenAI account has credits
3. Test API key:
   ```powershell
   curl https://api.openai.com/v1/models -H "Authorization: Bearer YOUR_API_KEY"
   ```

### Issue: Port Already in Use

**Error**: `Address already in use`

**Solution**:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use a different port
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

### Issue: Module Not Found

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Database Tables Not Created

**Error**: `relation "research_briefs" does not exist`

**Solution**:
The application automatically creates tables on startup. If this fails:

1. Check logs for errors
2. Verify database permissions
3. Manually create tables by running Python:
   ```powershell
   python -c "from app.database import init_db; init_db()"
   ```

## Development Tips

### View Logs

The application logs to console. Look for:
- `INFO` - Normal operations
- `WARNING` - Potential issues
- `ERROR` - Failures

### Database Inspection

```powershell
# Connect to database
psql $env:DATABASE_URL

# List tables
\dt

# View research briefs
SELECT id, status, created_at FROM research_briefs;

# View specific brief
SELECT * FROM research_briefs WHERE id = 'YOUR_BRIEF_ID';

# Exit
\q
```

### API Testing with curl

```powershell
# Health check
curl http://127.0.0.1:8000/status

# Submit URLs (PowerShell)
$body = @{
    urls = @(
        "https://example.com/article1",
        "https://example.com/article2"
    )
} | ConvertTo-Json

Invoke-RestMethod -Uri http://127.0.0.1:8000/submit -Method POST -Body $body -ContentType "application/json"
```

## Next Steps

Once local development is working:

1. ✅ Test all features thoroughly
2. ✅ Review code for any needed customizations
3. ✅ Update ABOUTME.md with your information
4. ✅ Follow README.md for Render deployment
5. ✅ Test deployed application

## Getting Help

If you encounter issues:

1. Check the logs for error messages
2. Review the troubleshooting section above
3. Verify all prerequisites are met
4. Check environment variables are correct
5. Ensure PostgreSQL and OpenAI services are accessible

## Success Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] PostgreSQL database created
- [ ] `.env` file configured with real credentials
- [ ] Database connection successful
- [ ] OpenAI API key validated
- [ ] Application starts without errors
- [ ] Health check returns all "ok"
- [ ] Can submit URLs and generate briefs
- [ ] Recent briefs display correctly

Once all items are checked, you're ready to deploy to Render!
