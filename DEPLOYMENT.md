# Deployment Guide

This document provides instructions for deploying the Genomic Twin platform to various cloud providers.

## Quick Start

### Local Development
```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Build the project
npm run build

# Start local server
python3 server.py
# Or for Streamlit development
npm run dev
```

Visit http://localhost:8000 for the web interface.

## Deployment Platforms

### Vercel (Recommended)
1. Connect your GitHub repository to Vercel
2. Vercel will automatically detect the `vercel.json` configuration
3. Deploy with zero configuration needed

**Manual deployment:**
```bash
npm install -g vercel
vercel --prod
```

### Netlify
1. Connect your GitHub repository to Netlify
2. Netlify will use the `netlify.toml` configuration
3. Build command: `npm run build`
4. Publish directory: `dist`

### Heroku
```bash
git push heroku main
```
Uses the `Procfile` for process configuration.

### Docker
```bash
docker build -t genomic-twin .
docker run -p 8000:8000 genomic-twin
```

## Environment Variables

For production deployments, you may need to set:

```bash
# Optional: Custom port
PORT=8000

# For Streamlit features
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## Health Checks

The platform provides health check endpoints:

- `GET /health` - Basic health status
- `GET /api/status` - Detailed API status

## Troubleshooting

### Common Deployment Issues

1. **404 Errors**: Ensure `index.html` exists and routing is configured
2. **Python Import Errors**: Check that all dependencies are in `requirements.txt`
3. **Node.js Build Failures**: Verify Node.js version >=16.x

### Platform-Specific Issues

**Vercel:**
- Ensure Python runtime is set to 3.9 in `vercel.json`
- Check function timeout limits for data processing

**Netlify:**
- Verify redirect rules in `netlify.toml`
- Check build logs for missing dependencies

**Heroku:**
- Ensure `Procfile` is correctly formatted
- Check dyno limits and scaling settings

## Architecture

The platform supports multiple deployment modes:

1. **Static Web App**: Basic HTML/CSS/JS interface
2. **Python Web Server**: HTTP server with API endpoints
3. **Streamlit App**: Interactive data science interface
4. **Hybrid Mode**: Combines static frontend with Python backend

## Monitoring

Monitor deployment health using:
- Platform-specific dashboards (Vercel Analytics, Netlify Analytics)
- Custom health check endpoints
- Application logs

## Security

- All sensitive data should be in environment variables
- HTTPS is enforced on all production deployments
- CORS is configured for API endpoints
- Input validation is implemented for all user inputs