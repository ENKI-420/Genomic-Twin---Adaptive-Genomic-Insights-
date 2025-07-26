# DNA-Lang: The Autonomous Bio-Digital Platform

An AI-powered platform that creates living digital twins—self-evolving, self-managing software organisms that provide adaptive genomic insights and autonomously orchestrate their own cloud infrastructure on Google Cloud.

## 🚀 One-Click Deploy to Google Cloud

Launch the entire platform, including the evolution engine, digital twin simulator, and dashboard, to your Google Cloud project in minutes.

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-in-cloud-shell.svg)](https://shell.cloud.google.com/cloudshell_open?git_repo=https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-&tutorial=README.md&shellonly=true)

After opening Cloud Shell, the setup script will guide you through an automated deployment.

## 🎯 Executive Summary

The DNA-Lang Autonomous Bio-Digital Platform represents a paradigm shift in both cloud computing and precision medicine. By treating genomic digital twins as living software organisms, we unlock the ability for them to evolve, adapt, and self-optimize in response to new data. Each organism autonomously provisions and scales its own secure cloud infrastructure, runs complex simulations, and provides real-time insights, creating a truly adaptive system for next-generation genomic analysis.

**Key Features:**

- **Living Digital Twins**: Organisms that model genomic data and evolve over time.
- **Autonomous Infrastructure**: Each organism provisions and manages its own secure GCP resources via Terraform.
- **Real-time Evolution Engine**: Organisms mutate and adapt based on new clinical data or research findings.
- **AI-Powered Agents**: A team of AI agents manages infrastructure, tracks lineage, and optimizes the ecosystem.
- **Interactive Dashboard**: A unified interface to monitor organism evolution, run simulations, and view genomic insights.

## 🏗️ Architecture

```
graph TD
    subgraph "User Interface"
        A[Streamlit/React Dashboard]
    end

    subgraph "Google Cloud Platform"
        B[Cloud Run: API & Evolution Engine]
        C[Cloud SQL: Genomic & State Data]
        D[Pub/Sub: Event Bus]
        E[Terraform: IaC Provisioner]
    end

    subgraph "Autonomous Agents"
        F[Cloud Architect Agent]
        G[Biography Agent]
        H[Meta-Cognition Agent]
    end

    A -- "API Calls / WebSocket" --> B
    B -- "Reads/Writes" --> C
    B -- "Publishes Events" --> D
    B -- "Triggers" --> E
    D -- "Triggers" --> F
    D -- "Triggers" --> G
    D -- "Triggers" --> H
```

## 🚀 Quick Start & Development

### 1. Prerequisites
- A Google Cloud Project with billing enabled.
- gcloud CLI, Node.js, and Python 3.10+ installed locally.

### 2. Cloud Deployment (Recommended)
Click the "Open in Cloud Shell" button above and follow the on-screen instructions. The script handles all API enablement and resource deployment.

### 3. Local Development

**Clone the repository:**
```bash
git clone https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-.git
cd Genomic-Twin---Adaptive-Genomic-Insights-
```

**Configure Environment:**
Copy `.env.example` to `.env` and fill in your GCP Project ID and local database credentials.

**Install Dependencies & Run:**
```bash
# Install backend (evolution engine & agents) dependencies
npm install

# Install frontend (dashboard) dependencies
pip install -r requirements.txt

# Start the backend services (in one terminal)
npm run start:backend

# Start the frontend dashboard (in another terminal)
streamlit run app.py
```

## 📁 Unified Project Structure

```
.
├── .github/workflows/      # CI/CD Pipeline for autonomous deployment
│   └── main.yml
├── backend/                # Node.js Evolution Engine & AI Agents
│   ├── agents/
│   ├── evolution_engine.js
│   └── cloud_provisioner.js
├── frontend/               # Python Streamlit Dashboard & UI
│   ├── app.py
│   └── requirements.txt
├── terraform/              # Master Terraform modules for GCP
│   └── main.tf
├── setup.sh                # Automated Cloud Shell deployment script
├── cloudbuild.yaml         # Production-ready CI/CD configuration
└── README.md               # This file
```

This structure cleanly separates the backend brain (the Node.js evolution engine) from the frontend interface (the Streamlit dashboard), while centralizing infrastructure and deployment automation.
