# Backend Environment Variables Setup

## Environment Variables

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
# For development
CORS_ORIGINS=http://127.0.0.1:3000,http://localhost:3000

# For production, add your frontend URL
# CORS_ORIGINS=https://gradematelk.vercel.app,https://*.vercel.app
```

## Production Deployment

When deploying your backend to a hosting service (Railway, Render, Heroku, etc.), set these environment variables:

1. **Database**: Update with your production database credentials
2. **Environment**: Set to `production`
3. **CORS Origins**: Include your Vercel frontend URL and any preview URLs

## CORS Configuration

The backend is configured to allow requests from:
- Local development URLs (`http://127.0.0.1:3000`, `http://localhost:3000`)
- Your production frontend (`https://gradematelk.vercel.app`)
- All Vercel preview deployments (`https://*.vercel.app`)

## Security Notes

- In production, avoid using `allow_origins=["*"]` for security
- The current configuration allows credentials, which is needed for authentication
- Make sure to update CORS_ORIGINS when deploying to production
