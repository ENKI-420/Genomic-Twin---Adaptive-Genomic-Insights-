# Genomic Twin - Adaptive Genomic Insights Platform

An AI-powered platform for oncology, offering tools for mutation analysis, digital twin simulations, CRISPR feasibility, and more.

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Build the project
npm run build

# Start the web server
python3 server.py
# Visit http://localhost:8000

# OR start Streamlit development server
npm run dev
# Visit http://localhost:8501
```

### Deployment

This platform is ready for deployment on multiple platforms:

- **Vercel**: Zero-config deployment with `vercel.json`
- **Netlify**: Configured with `netlify.toml`
- **Heroku**: Uses `Procfile` for process management
- **Docker**: Build and run with `docker-compose up`

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🧬 Platform Features

### Core Modules
- **Clinical Dashboard** - Patient data management and visualization
- **Digital Twin Simulation** - AI-powered patient modeling
- **CRISPR Feasibility** - Gene editing analysis and recommendations
- **Nanoparticle Delivery** - Drug delivery system optimization
- **Blockchain Monitoring** - Secure data tracking and verification
- **Market Analytics** - Oncology market insights and trends

### Deployment Features
- ✅ Multi-platform deployment support
- ✅ Health check endpoints (`/health`, `/api/status`)
- ✅ Static web interface with interactive visualizations
- ✅ Python/Streamlit backend for data analysis
- ✅ Node.js components for real-time processing
- ✅ Docker containerization
- ✅ CI/CD ready configurations

## 🔗 API Endpoints

- `GET /` - Main web interface
- `GET /health` - System health check
- `GET /api/status` - Detailed API status
- `GET /lineage` - Digital organism lineage visualizer

## 🛠 Development

### Architecture
- **Frontend**: HTML/CSS/JavaScript with modern UI
- **Backend**: Python (Streamlit) + Node.js components
- **Deployment**: Multi-cloud ready with platform-specific configurations

### Technology Stack
- Python 3.9+ with Streamlit
- Node.js 16+ with WebSocket support
- Modern web standards (HTML5, CSS3, ES6+)
- Cloud-native deployment patterns

## 📊 Monitoring

The platform includes built-in monitoring:
- Health check endpoints for uptime monitoring
- Deployment status validation
- Error logging and debugging support

## 🔒 Security

- HTTPS enforcement on production deployments
- Input validation for all user interfaces
- Environment variable configuration for sensitive data
- CORS configuration for API access

---

*Developed by ENKI-420 | Licensed under MIT*
