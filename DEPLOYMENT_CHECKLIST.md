# Render Deployment Checklist

Use this checklist to ensure successful deployment to Render.

## Pre-Deployment Checklist

### Code Preparation
- [ ] All code committed to Git repository
- [ ] `.env` file is in `.gitignore` (verify it's not committed)
- [ ] `requirements.txt` has all dependencies with pinned versions
- [ ] `ABOUTME.md` updated with your information
- [ ] Code tested locally and working

### Render Account Setup
- [ ] Created Render account at https://render.com
- [ ] Verified email address
- [ ] Connected GitHub/GitLab account to Render

### OpenAI Setup
- [ ] Have valid OpenAI API key
- [ ] API key has credits available
- [ ] Tested API key locally

## Deployment Steps

### Step 1: Create PostgreSQL Database ✅

- [ ] Logged into Render Dashboard
- [ ] Clicked "New +" → "PostgreSQL"
- [ ] Configured database:
  - [ ] Name: `research-brief-db` (or your choice)
  - [ ] Database: `research_brief_db`
  - [ ] User: (auto-generated)
  - [ ] Region: Selected closest region
  - [ ] Plan: Selected Free or paid plan
- [ ] Clicked "Create Database"
- [ ] Waited for database to be created (1-2 minutes)
- [ ] **Copied Internal Database URL** (starts with `postgresql://`)
  - Format: `postgresql://user:password@host/database`
  - Save this securely!

### Step 2: Create Web Service ✅

- [ ] Clicked "New +" → "Web Service"
- [ ] Selected "Build and deploy from a Git repository"
- [ ] Connected repository:
  - [ ] Selected your Git repository
  - [ ] Authorized Render to access repository
- [ ] Configured web service:
  - [ ] **Name**: `research-brief-app` (or your choice)
  - [ ] **Region**: Same as database (important!)
  - [ ] **Branch**: `main` or `master`
  - [ ] **Root Directory**: (leave blank if project is in root)
  - [ ] **Runtime**: `Python 3`
  - [ ] **Build Command**: `pip install -r requirements.txt`
  - [ ] **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`

### Step 3: Set Environment Variables ✅

Click "Advanced" → "Add Environment Variable" for each:

- [ ] `DATABASE_URL`
  - Value: (Paste Internal Database URL from Step 1)
  - Example: `postgresql://user:pass@host/research_brief_db`

- [ ] `OPENAI_API_KEY`
  - Value: (Your OpenAI API key)
  - Example: `sk-proj-...`

- [ ] `ENVIRONMENT`
  - Value: `production`

- [ ] `PORT`
  - Value: `10000`

- [ ] `PYTHON_VERSION`
  - Value: `3.11.0`

**Double-check all values before proceeding!**

### Step 4: Deploy ✅

- [ ] Reviewed all settings
- [ ] Clicked "Create Web Service"
- [ ] Deployment started automatically

### Step 5: Monitor Deployment ✅

- [ ] Watched build logs in Render dashboard
- [ ] Build completed successfully (green checkmark)
- [ ] Service status shows "Live"
- [ ] Noted the deployment URL (e.g., `https://research-brief-app.onrender.com`)

## Post-Deployment Verification

### Health Check ✅

- [ ] Visited `https://your-app.onrender.com/status`
- [ ] Received response:
  ```json
  {
    "backend": "ok",
    "database": "ok",
    "llm": "ok"
  }
  ```
- [ ] All three status checks show "ok"

### Functional Testing ✅

- [ ] Visited home page: `https://your-app.onrender.com/`
- [ ] Page loads correctly with form
- [ ] Submitted test URLs:
  ```
  https://en.wikipedia.org/wiki/Artificial_intelligence
  https://en.wikipedia.org/wiki/Machine_learning
  ```
- [ ] Redirected to brief page
- [ ] Processing spinner appeared
- [ ] Page auto-refreshed
- [ ] Research brief generated successfully
- [ ] All sections displayed:
  - [ ] Summary
  - [ ] Key Points
  - [ ] Conflicting Claims (if any)
  - [ ] Verification Checklist
  - [ ] Sources
- [ ] Returned to home page
- [ ] Recent brief appears in "Recent Research Briefs"
- [ ] Clicked on recent brief
- [ ] Brief displays correctly

### Error Handling Testing ✅

- [ ] Submitted invalid URL
- [ ] Error message displayed correctly
- [ ] Submitted more than 10 URLs
- [ ] Validation error displayed
- [ ] Application recovered gracefully

### Mobile Testing ✅

- [ ] Opened app on mobile device
- [ ] Layout is responsive
- [ ] Form works on mobile
- [ ] Results page readable on mobile

## Troubleshooting

### Build Failed

**Check**:
- [ ] `requirements.txt` is in repository root
- [ ] All dependencies are valid
- [ ] Python version is compatible

**Fix**:
- Review build logs in Render dashboard
- Fix any dependency issues
- Push changes to Git
- Render will auto-deploy

### Database Connection Error

**Check**:
- [ ] `DATABASE_URL` environment variable is set
- [ ] Database URL is the **Internal** URL (not External)
- [ ] Database and web service are in same region
- [ ] Database is running (check Render dashboard)

**Fix**:
- Verify DATABASE_URL in environment variables
- Copy Internal Database URL again from database dashboard
- Update environment variable
- Manually deploy from Render dashboard

### OpenAI API Error

**Check**:
- [ ] `OPENAI_API_KEY` environment variable is set
- [ ] API key is valid (no typos)
- [ ] OpenAI account has credits
- [ ] API key has correct permissions

**Fix**:
- Test API key at https://platform.openai.com/playground
- Generate new API key if needed
- Update environment variable
- Manually deploy

### Application Not Starting

**Check**:
- [ ] Start command is correct: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
- [ ] PORT environment variable is set to `10000`
- [ ] Application binds to `0.0.0.0` (check `app/main.py`)

**Fix**:
- Review application logs in Render dashboard
- Verify start command
- Check for Python errors in logs
- Fix issues and push to Git

### Slow First Request

**Note**: This is normal on Render's free tier!
- Free tier services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Subsequent requests are fast

**Solutions**:
- Upgrade to paid plan (services stay running)
- Accept the delay on free tier
- Use a service like UptimeRobot to ping your app

## Performance Optimization

### After Successful Deployment

- [ ] Monitor application logs for errors
- [ ] Check OpenAI API usage and costs
- [ ] Monitor database size
- [ ] Set up error alerting (optional)
- [ ] Configure custom domain (optional)

### Render Dashboard Monitoring

- [ ] Bookmarked Render dashboard
- [ ] Checked "Metrics" tab for:
  - [ ] CPU usage
  - [ ] Memory usage
  - [ ] Request count
  - [ ] Response times
- [ ] Reviewed logs regularly

## Cost Monitoring

### Free Tier Limits

**PostgreSQL**:
- [ ] 1 GB storage
- [ ] Expires after 90 days
- [ ] Monitor database size

**Web Service**:
- [ ] 750 hours/month
- [ ] Spins down after inactivity
- [ ] 100 GB bandwidth/month

**OpenAI**:
- [ ] Pay-per-use
- [ ] Monitor at https://platform.openai.com/usage
- [ ] Set spending limits

### Cost Optimization

- [ ] Use GPT-4o-mini (cheaper than GPT-4)
- [ ] Limit content length (5000 chars per article)
- [ ] Monitor API usage regularly
- [ ] Consider caching results (future enhancement)

## Security Checklist

- [ ] `.env` file not in Git repository
- [ ] Environment variables set in Render dashboard only
- [ ] No API keys in code
- [ ] No hardcoded secrets
- [ ] HTTPS enabled (automatic on Render)

## Documentation

- [ ] Deployment URL documented
- [ ] Environment variables documented
- [ ] Any custom configurations noted
- [ ] Known issues documented

## Final Verification

- [ ] Application is live and accessible
- [ ] All features working correctly
- [ ] Health check passes
- [ ] No errors in logs
- [ ] Performance is acceptable
- [ ] Mobile responsive
- [ ] Documentation complete

## Submission Checklist

For assignment submission:

- [ ] Deployment URL: `https://your-app.onrender.com`
- [ ] GitHub repository URL
- [ ] README.md complete
- [ ] All documentation files included
- [ ] ABOUTME.md updated with your information
- [ ] Screenshots of working application (optional)
- [ ] Video demo (optional)

## Maintenance Schedule

### Daily
- [ ] Check application is running
- [ ] Review error logs

### Weekly
- [ ] Monitor OpenAI costs
- [ ] Check database size
- [ ] Review performance metrics

### Monthly
- [ ] Update dependencies if needed
- [ ] Review and optimize costs
- [ ] Backup important data

## Support Resources

If you encounter issues:

1. **Render Documentation**: https://render.com/docs
2. **Render Community**: https://community.render.com
3. **FastAPI Documentation**: https://fastapi.tiangolo.com
4. **OpenAI Support**: https://help.openai.com

## Success! 🎉

Once all items are checked:

✅ Your application is successfully deployed to Render!
✅ It's accessible via public URL
✅ All features are working
✅ You're ready to submit your assignment

**Deployment URL**: _______________________________

**Deployed on**: _______________________________

**Notes**: 
_____________________________________________
_____________________________________________
_____________________________________________

---

**Congratulations on your successful deployment!** 🚀
