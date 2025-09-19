# Backend Environment Variables Setup

## Local Development

Create a `.env` file in the Backend directory with the following variables:

```bash
# Database Configuration
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASS=password
DB_NAME=hackathon_db

# Environment
ENVIRONMENT=development

# CORS Origins (comma-separated list)
CORS_ORIGINS=http://127.0.0.1:3000,http://localhost:3000,https://gradematelk.vercel.app,https://*.vercel.app
```

## Running Locally

You can run the backend locally using either:

```bash
# Option 1: Using the startup script
python start.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Render Deployment

### 1. Deploy to Render

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Use the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python start.py`
   - **Environment**: `Python 3`

### 2. Environment Variables in Render

Set these environment variables in your Render dashboard:

```bash
# Required
ENVIRONMENT=production
CORS_ORIGINS=https://gradematelk.vercel.app,https://*.vercel.app

# Database (update with your production database)
DB_HOST=your-production-db-host
DB_PORT=3306
DB_USER=your-db-user
DB_PASS=your-db-password
DB_NAME=your-db-name

# Render automatically sets:
# PORT (automatically set by Render)
# RENDER_EXTERNAL_URL (automatically set by Render)
```

### 3. Update Frontend

After deploying to Render, update your Vercel environment variables:

1. Go to Vercel Dashboard → Project Settings → Environment Variables
2. Add/Update: `VITE_API_BASE_URL=https://your-render-app-name.onrender.com`

## CORS Configuration

The backend automatically configures CORS based on environment:

**Development Mode:**
- `http://127.0.0.1:3000`
- `http://localhost:3000`
- Plus any origins in `CORS_ORIGINS`

**Production Mode:**
- Origins specified in `CORS_ORIGINS` environment variable
- Your Render URL (automatically added)
- Your Vercel frontend URL

## Files for Deployment

- `render.yaml` - Render deployment configuration
- `start.py` - Production startup script
- `requirements.txt` - Python dependencies

## Security Notes

- CORS origins are explicitly configured (no wildcard `*`)
- Credentials are allowed for authentication
- Environment-specific configurations prevent development settings in production
