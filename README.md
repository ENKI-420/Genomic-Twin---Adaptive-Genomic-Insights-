# DNA-Lang Genomic Twin - Adaptive Genomic Insights Platform

An AI-powered genomic analysis platform offering tools for mutation analysis, digital twin simulations, clinical trial matching, and advanced genomic insights with seamless Google Cloud deployment.

## 🚀 Quick Deploy to Google Cloud

Deploy the complete DNA-Lang ecosystem to Google Cloud with just one click:

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-in-cloud-shell.svg)](https://shell.cloud.google.com/cloudshell_open?git_repo=https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-&tutorial=README.md&shellonly=true)

After opening Cloud Shell, run:
```bash
chmod +x setup.sh && ./setup.sh
```

## 🏗️ Deployment Options

### Option 1: One-Click Cloud Shell Deployment (Recommended for Quick Start)
Perfect for demos and rapid deployment. Uses our automated setup script to deploy everything in minutes.

**Features:**
- Interactive Google Cloud project selection
- Automated API enablement
- Cloud SQL PostgreSQL database setup
- Pub/Sub event processing
- Cloud Run containerized deployment
- Automatic scaling and load balancing

### Option 2: Terraform + Cloud Build (Production Ready)
Robust Infrastructure as Code approach for scalable, repeatable deployments.

**Prerequisites:**
- Google Cloud Project with billing enabled
- Cloud Build API enabled
- Terraform knowledge (optional)

**Deploy using Cloud Build:**
1. Fork this repository
2. Create a Cloud Build trigger pointing to `cloudbuild.yaml`
3. Run the trigger with your project ID
4. Monitor deployment in Cloud Build console

### Option 3: Google Cloud Marketplace (Coming Soon)
Enterprise-grade deployment with integrated billing and subscription management.

## 🧬 Platform Modules

- **Genomic Analysis Engine** - Advanced mutation analysis and interpretation
- **Digital Twin Simulation** - Patient-specific genomic modeling
- **Clinical Trial Matching** - AI-powered trial recommendation
- **CRISPR Feasibility Analysis** - Gene editing potential assessment
- **Nanoparticle Delivery Optimization** - Targeted therapy design
- **Blockchain Genomic Monitoring** - Secure, traceable genomic data
- **Market Analytics Dashboard** - Genomic trends and insights

## 🛠️ Local Development

### Prerequisites
- Python 3.10+
- Node.js 16+
- Google Cloud SDK (optional for local testing)

### Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Run the Streamlit application
streamlit run app.py

# Run individual AI agents
npm run bio          # Biography agent
npm run meta         # Meta-cognition agent
npm run lineage      # Lineage generator
```

### Environment Variables
Create a `.env` file with:
```env
DATABASE_URL=postgresql://username:password@localhost/genomic_twin_db
PROJECT_ID=your-gcp-project-id
PUBSUB_TOPIC=dnalang-genomic-events
EPIC_API_URL=https://fhir.epic.com/interconnect-fhir-oauth
```

## 📊 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Cloud Run      │    │   Cloud SQL     │
│   Frontend      │────│   Application    │────│   PostgreSQL    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌────────────────┐              │
         └──────────────│   Pub/Sub      │──────────────┘
                        │   Event Bus    │
                        └────────────────┘
                                 │
                    ┌─────────────────────────┐
                    │   AI Processing         │
                    │   - Biography Agent     │
                    │   - Meta-Cognition      │
                    │   - Evolution Engine    │
                    └─────────────────────────┘
```

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `setup.sh` | One-click deployment script |
| `Dockerfile` | Container configuration |
| `cloudbuild.yaml` | CI/CD pipeline configuration |
| `terraform/` | Infrastructure as Code |
| `main.tf` | Legacy Terraform (preserved) |

## 📚 API Documentation

### Genomic Analysis Endpoints
- `POST /analyze` - Upload and analyze genomic data
- `GET /reports/{id}` - Retrieve analysis reports
- `POST /digital-twin` - Generate patient digital twin
- `GET /trials/{patient_id}` - Find matching clinical trials

### WebSocket Events
- `genomic_analysis_complete` - Analysis finished
- `digital_twin_updated` - Twin model updated
- `trial_match_found` - New trial match
- `evolution_step` - AI evolution progress

## 🧪 Testing

```bash
# Run Python tests
python -m pytest tests/

# Run Node.js tests  
npm test

# Test deployment locally
docker build -t dnalang-test .
docker run -p 8080:8080 dnalang-test
```

## 🔒 Security & Compliance

- **HIPAA Compliant** - Secure genomic data handling
- **SOC 2 Type II** - Enterprise security standards
- **GDPR Ready** - EU data protection compliance
- **Encryption** - Data encrypted at rest and in transit
- **IAM Integration** - Google Cloud identity management

## 🚀 Production Deployment

### Scaling Configuration
- **Auto-scaling**: 0-100 instances based on traffic
- **Memory**: 2-8GB per instance (configurable)
- **CPU**: 1-4 vCPUs per instance
- **Database**: Scalable Cloud SQL with read replicas

### Monitoring & Observability
- Cloud Monitoring dashboards
- Structured logging with Cloud Logging
- Error reporting and alerting
- Performance metrics and SLA monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [Wiki](https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/wiki)
- **Issues**: [GitHub Issues](https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/discussions)
- **Email**: support@dnalang.io (coming soon)

---

**🧬 Empowering Precision Medicine through AI-Driven Genomic Insights**
