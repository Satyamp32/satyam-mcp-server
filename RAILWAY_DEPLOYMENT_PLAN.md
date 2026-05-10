# 🚀 Railway Deployment Plan - Google Docs + Gmail MCP Server

## 📋 Overview

This document outlines the complete deployment strategy for the Google Docs + Gmail MCP Server on Railway. The deployment includes environment configuration, authentication setup, and deployment procedures.

## 🏗️ Architecture

### Local Development
- Manual OAuth authentication flow
- Local file-based credential storage
- CLI-based approval system

### Railway Deployment
- Environment variable-based authentication
- Auto-approval system for production
- Container-based deployment with Docker
- Health checks and monitoring

## 📁 Files Created/Modified

### New Files
- `railway.toml` - Railway configuration
- `Dockerfile` - Container configuration
- `.dockerignore` - Docker build optimization
- `RAILWAY_DEPLOYMENT_PLAN.md` - This documentation

### Modified Files
- `auth.py` - Updated for Railway environment detection
- `server.py` - Enhanced approval system for Railway

## 🔧 Railway Configuration

### railway.toml
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn server:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/"
healthcheckTimeout = 100
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10

[env]
PYTHON_VERSION = "3.11.9"
AUTO_APPROVE = "true"
PORT = "8000"
```

### Dockerfile
- Uses Python 3.11.9 slim image
- Multi-stage build optimization
- Non-root user for security
- Health checks enabled
- Proper port exposure

## 🔐 Authentication Setup

### Required Environment Variables

1. **GOOGLE_CREDENTIALS_JSON**
   - OAuth client credentials from Google Cloud Console
   - Must be JSON format
   - Set in Railway dashboard

2. **GOOGLE_TOKEN_JSON**
   - Refresh token for OAuth
   - Generated from local OAuth flow
   - Set in Railway dashboard

### Environment Detection
The application automatically detects Railway environment using:
- `RAILWAY_ENVIRONMENT`
- `RAILWAY_SERVICE_NAME`
- `RAILWAY_PROJECT_NAME`

## 🚀 Deployment Steps

### 1. Pre-Deployment Setup

#### Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select/create project
3. Enable APIs:
   - Google Docs API
   - Gmail API
4. Configure OAuth Consent Screen
5. Create OAuth Credentials (Desktop App)
6. Download `credentials.json`

#### Generate Refresh Token
```bash
# Run locally to generate token.json
python3 auth.py
```

### 2. Railway Project Setup

1. **Create Railway Account**
   - Sign up at [railway.app](https://railway.app)
   - Install Railway CLI (optional)

2. **Create New Project**
   - Click "New Project" in Railway dashboard
   - Choose "Deploy from GitHub repo"

3. **Connect Repository**
   - Connect your GitHub repository
   - Select the MCP server repository

### 3. Environment Variables Configuration

In Railway dashboard, add these variables:

#### Required Variables
```bash
GOOGLE_CREDENTIALS_JSON={"installed":{"client_id":"your_client_id","client_secret":"your_client_secret","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","redirect_uris":["http://localhost"]}}

GOOGLE_TOKEN_JSON={"token":"your_refresh_token","refresh_token":"your_refresh_token","token_uri":"https://oauth2.googleapis.com/token","client_id":"your_client_id","client_secret":"your_client_secret","scopes":["https://www.googleapis.com/auth/documents","https://www.googleapis.com/auth/gmail.compose"],"expiry_date":"2024-01-01T00:00:00Z"}
```

#### Optional Variables
```bash
AUTO_APPROVE=true
PYTHON_VERSION=3.11.9
PORT=8000
```

### 4. Deployment Process

1. **Automatic Deployment**
   - Railway will automatically detect changes
   - Build process starts automatically
   - Application deploys to Railway infrastructure

2. **Manual Deployment**
   ```bash
   # Using Railway CLI
   railway up
   
   # Or trigger deployment from Railway dashboard
   ```

### 5. Health Check Verification

After deployment, verify:
- Application starts successfully
- Health check endpoint responds: `https://your-app.railway.app/`
- API documentation accessible: `https://your-app.railway.app/docs`

## 🧪 Testing

### Local Testing
```bash
# Test locally before deployment
uvicorn server:app --reload
curl http://localhost:8000/
```

### Railway Testing
```bash
# Test deployed application
curl https://your-app.railway.app/
curl https://your-app.railway.app/docs
```

### API Testing
```bash
# Test append to doc endpoint
curl -X POST "https://your-app.railway.app/append_to_doc" \
  -H "Content-Type: application/json" \
  -d '{
    "doc_id": "your_doc_id",
    "content": "Test from Railway deployment"
  }'

# Test email draft endpoint
curl -X POST "https://your-app.railway.app/create_email_draft" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "test@example.com",
    "subject": "Test from Railway",
    "body": "This is a test email"
  }'
```

## 🔍 Monitoring & Logging

### Railway Dashboard
- View deployment logs
- Monitor resource usage
- Check health status
- Access application metrics

### Application Logs
- Structured logging with timestamps
- Error tracking and reporting
- Request/response logging
- Authentication flow logging

## 🚨 Troubleshooting

### Common Issues

#### 1. Authentication Failures
**Symptoms:** 401/403 errors from Google APIs
**Solutions:**
- Verify `GOOGLE_CREDENTIALS_JSON` format
- Check `GOOGLE_TOKEN_JSON` validity
- Ensure OAuth app has required scopes
- Refresh token may have expired

#### 2. Build Failures
**Symptoms:** Deployment fails during build
**Solutions:**
- Check `requirements.txt` for valid dependencies
- Verify Dockerfile syntax
- Check Railway build logs

#### 3. Health Check Failures
**Symptoms:** Application marked as unhealthy
**Solutions:**
- Verify port binding (use 0.0.0.0)
- Check health check endpoint
- Monitor application startup time

#### 4. Environment Variable Issues
**Symptoms:** Configuration errors
**Solutions:**
- Verify variable names and formats
- Check JSON syntax for credential variables
- Ensure no trailing spaces or special characters

### Debug Commands
```bash
# Check Railway logs
railway logs

# View deployed environment
railway variables

# Restart deployment
railway restart
```

## 🔄 CI/CD Integration

### GitHub Actions (Optional)
```yaml
name: Deploy to Railway
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        uses: railway-app/railway-action@v1
        with:
          api-token: ${{ secrets.RAILWAY_TOKEN }}
          service-id: ${{ secrets.RAILWAY_SERVICE_ID }}
```

## 📊 Performance Considerations

### Optimization Tips
1. **Cold Starts:** Use Railway's hobby tier for better performance
2. **Memory Usage:** Monitor Google API client memory consumption
3. **Rate Limiting:** Implement request rate limiting for Google APIs
4. **Caching:** Cache Google API responses where appropriate

### Scaling
- Railway automatically scales based on demand
- Monitor resource usage in dashboard
- Consider upgrading plan for high-traffic applications

## 🔒 Security Best Practices

1. **Environment Variables:** Never commit credentials to repository
2. **OAuth Scopes:** Use minimum required scopes
3. **Token Storage:** Use Railway's encrypted environment variables
4. **Network Security:** Railway provides HTTPS by default
5. **Access Control:** Implement API authentication if needed

## 📝 Maintenance

### Regular Tasks
1. **Token Refresh:** Monitor OAuth token expiration
2. **Dependency Updates:** Keep Python packages updated
3. **API Changes:** Monitor Google API changes/deprecations
4. **Log Monitoring:** Regularly check application logs
5. **Performance Monitoring:** Track application performance

### Backup Strategy
- Export Railway environment variables regularly
- Backup Google OAuth configuration
- Document any custom configurations

## 🎯 Success Criteria

### Deployment Success Indicators
- ✅ Application starts without errors
- ✅ Health check passes
- ✅ API endpoints respond correctly
- ✅ OAuth authentication works
- ✅ Google API integration functions
- ✅ Auto-approval system works in deployment

### Performance Metrics
- Application startup time < 30 seconds
- API response time < 2 seconds
- 99%+ uptime
- Zero authentication failures

## 📞 Support

### Resources
- [Railway Documentation](https://docs.railway.app/)
- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google APIs Documentation](https://developers.google.com/apis)

### Emergency Contacts
- Railway Support: support@railway.app
- Google Cloud Support: Available through Google Cloud Console

---

**Last Updated:** May 2026
**Version:** 1.0
**Maintainer:** MCP Server Team
