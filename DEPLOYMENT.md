# JuSimples Deployment Guide

This guide will help you deploy your JuSimples Legal AI Platform to production using Netlify for the frontend and a cloud service for the backend.

## 🏗️ Architecture Overview

- **Frontend**: React app deployed on Netlify
- **Backend**: Python Flask API deployed on Railway/Render/Heroku
- **Database**: ChromaDB (local file-based for MVP)
- **AI**: OpenAI GPT-4 API

## 📋 Prerequisites

- GitHub repository with your code
- Netlify account
- Railway/Render account for backend
- OpenAI API key

## 🚀 Frontend Deployment (Netlify)

### Step 1: Connect Repository to Netlify

1. Go to [Netlify](https://app.netlify.com)
2. Click "New site from Git"
3. Choose GitHub and authorize access
4. Select your `jusimples` repository

### Step 2: Configure Build Settings

Use these exact settings in Netlify:

- **Base directory**: `frontend`
- **Build command**: `npm install && npm run build`
- **Publish directory**: `frontend/build`

### Step 3: Environment Variables

Add these environment variables in Netlify dashboard:

```
REACT_APP_API_URL=https://your-backend-url.com
REACT_APP_ENVIRONMENT=production
REACT_APP_NAME=JuSimples
REACT_APP_VERSION=2.0.0
```

**Note**: Replace `your-backend-url.com` with your actual backend URL after backend deployment.

### Step 4: Deploy

Click "Deploy site" - Netlify will automatically build and deploy your frontend.

## 🔧 Backend Deployment Options

### Option A: Railway (Recommended)

1. Go to [Railway](https://railway.app)
2. Connect your GitHub repository
3. Select the backend folder
4. Configure environment variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   FLASK_ENV=production
   PORT=8080
   CORS_ORIGINS=https://your-netlify-site.netlify.app
   ```

### Option B: Render

1. Go to [Render](https://render.com)
2. Create new Web Service
3. Connect your repository
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python start_backend.py`

### Option C: Heroku

1. Install Heroku CLI
2. Create Procfile in backend folder:
   ```
   web: python start_backend.py
   ```
3. Deploy using Git:
   ```bash
   heroku create jusimples-api
   heroku config:set OPENAI_API_KEY=your_key
   git subtree push --prefix backend heroku main
   ```

## 🔄 Update Frontend with Backend URL

After backend deployment:

1. Get your backend URL (e.g., `https://jusimples-api.railway.app`)
2. Update Netlify environment variables:
   ```
   REACT_APP_API_URL=https://your-actual-backend-url.com
   ```
3. Update `netlify.toml` and `frontend/public/_redirects` with actual URL
4. Redeploy frontend

## 🛠️ Production Checklist

### Frontend
- [ ] Environment variables configured
- [ ] CORS headers set
- [ ] SPA routing configured
- [ ] Static assets cached
- [ ] Security headers enabled

### Backend
- [ ] OpenAI API key configured
- [ ] CORS origins updated
- [ ] Production logging enabled
- [ ] Error handling implemented
- [ ] Health check endpoint working

### Security
- [ ] API keys in environment variables (not code)
- [ ] CORS properly configured
- [ ] HTTPS enabled
- [ ] Security headers set

## 📊 Monitoring & Maintenance

### Frontend (Netlify)
- Monitor build logs in Netlify dashboard
- Set up form notifications for errors
- Monitor Core Web Vitals

### Backend
- Monitor application logs
- Set up health check monitoring
- Monitor API response times
- Monitor OpenAI API usage

## 🚨 Troubleshooting

### Common Issues

**1. Build Fails on Netlify**
- Check Node.js version (should be 18+)
- Verify all dependencies in package.json
- Check build logs for errors

**2. API Calls Fail**
- Verify REACT_APP_API_URL is correct
- Check CORS configuration on backend
- Verify backend is running and healthy

**3. Backend Deployment Issues**
- Check Python version compatibility
- Verify all dependencies in requirements.txt
- Check environment variables are set

## 🔧 Configuration Files Created

- `netlify.toml`: Main Netlify configuration
- `frontend/.env.example`: Environment variables template
- `frontend/public/_redirects`: SPA routing and API proxy
- `frontend/public/_headers`: Security headers
- Backend updated with CORS configuration

## 🌐 DNS & Custom Domain (Optional)

1. Purchase domain (e.g., jusimples.com.br)
2. Configure DNS in Netlify
3. Set up SSL certificate (automatic)
4. Update environment variables with new domain

## 📈 Scaling Considerations

### Frontend
- Enable Netlify CDN
- Optimize images and assets
- Implement code splitting

### Backend
- Use production WSGI server (Gunicorn)
- Implement caching (Redis)
- Scale database (PostgreSQL)
- Use production vector database (Pinecone)

---

**Next Steps**: Deploy backend first, then update frontend configuration with the backend URL.
