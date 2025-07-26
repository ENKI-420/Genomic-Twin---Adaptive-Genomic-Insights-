# DNA-Lang Live Digital Ecosystem

A living, breathing digital ecosystem where DNA-like organisms evolve, mutate, and trade genetic material in real-time while autonomously managing their own cloud infrastructure.

## 🧬 Overview

The DNA-Lang Live Digital Ecosystem showcases:

- **Autonomous DNA Sequence Evolution**: Self-mutating genetic sequences with emergent behaviors
- **Real-time Cloud Infrastructure**: Organisms automatically provision their own GCP resources via Terraform
- **Live Agent Collaboration**: AI agents (cloud architect, biography tracker, meta-cognition) work together
- **Interactive Dashboard**: Real-time visualization of evolution, lineage, and marketplace activity
- **Gene Marketplace**: Organisms trade genetic enhancements in a living economy

## 🚀 Quick Start

### 1. **Clone and Setup**

```bash
git clone https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-.git
cd Genomic-Twin---Adaptive-Genomic-Insights-
```

### 2. **Backend Setup**

```bash
cd backend
npm install
cp .env.example .env    # Configure your environment variables
node index.js           # Start the evolution engine and WebSocket server
```

The backend will start on `http://localhost:8081` with WebSocket on port `8082`.

### 3. **Frontend Setup** 

```bash
cd frontend
npm install
npm start               # Start the React dashboard
```

The dashboard will open at `http://localhost:3000` and connect to the backend automatically.

### 4. **Watch Evolution Happen**

- Visit the dashboard to see organisms evolving in real-time
- Watch the lineage tree grow as organisms reproduce and mutate
- Observe genes being traded in the marketplace
- See cloud infrastructure being provisioned automatically

## 🏗️ Architecture

### Backend Components

- **Evolution Engine**: Manages organism lifecycle, mutations, and emergent behaviors
- **Agent Manager**: Orchestrates AI agents (cloud_architect, biography, meta_cognition)
- **Event Bus**: Real-time communication between all system components
- **Cloud Provisioner**: Automatically generates and applies Terraform configurations
- **WebSocket Server**: Streams live updates to connected clients

### Frontend Components

- **Organism View**: Real-time organism dashboard with fitness and consciousness metrics
- **Lineage View**: Interactive evolutionary tree visualization
- **Marketplace View**: Gene trading interface with agent controls
- **Metrics View**: Population statistics and system health monitoring

## ☁️ Cloud Deployment

### Google Cloud Setup

1. **Enable required APIs**:
   ```bash
   gcloud services enable compute.googleapis.com
   gcloud services enable container.googleapis.com
   gcloud services enable sql-component.googleapis.com
   gcloud services enable redis.googleapis.com
   ```

2. **Set environment variables**:
   ```bash
   export GOOGLE_PROJECT_ID="your-project-id"
   export CLOUD_SQL_INSTANCE="your-cloud-sql-instance"
   export REDIS_HOST="your-redis-host"
   ```

3. **Deploy with GitHub Actions**:
   - Push changes to `main` branch
   - GitHub Actions will automatically deploy backend to Cloud Run and frontend to Vercel
   - Terraform will provision required GCP resources

### Manual Deployment

#### Backend to Cloud Run:
```bash
cd backend
gcloud builds submit --tag gcr.io/$GOOGLE_PROJECT_ID/dna-lang-backend
gcloud run deploy dna-lang-backend \
  --image gcr.io/$GOOGLE_PROJECT_ID/dna-lang-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Frontend to Vercel:
```bash
cd frontend
npm run build
npx vercel --prod
```

## 🧪 Development

### Running Tests
```bash
# Backend tests
cd backend && npm test

# Frontend tests  
cd frontend && npm test
```

### Building for Production
```bash
# Backend production build
cd backend && npm ci --production

# Frontend production build
cd frontend && npm run build
```

## 🎯 Key Features

### Real-time Evolution
- Organisms automatically mutate and evolve
- Fitness and consciousness levels tracked in real-time
- Emergent behaviors develop naturally
- Population dynamics with birth, reproduction, and death

### Autonomous Infrastructure
- Organisms automatically provision cloud resources when needed
- Terraform configurations generated and applied dynamically
- Infrastructure scales based on organism complexity and needs
- Complete infrastructure as code automation

### Interactive Dashboard
- Live visualization of all ecosystem activity
- Real-time lineage trees showing evolutionary relationships
- Gene marketplace with AI agent interactions
- Comprehensive metrics and system health monitoring

### Agent Collaboration
- **Cloud Architect**: Manages infrastructure provisioning and scaling
- **Biography Agent**: Tracks organism history and lineage relationships  
- **Meta Cognition**: Optimizes system performance and decision making

## 🔧 Environment Configuration

### Backend Environment (.env)
```bash
# Google Cloud Configuration
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_CLOUD_REGION=us-central1
CLOUD_SQL_INSTANCE=your-cloud-sql-instance
REDIS_HOST=your-redis-host

# Server Configuration
PORT=8081
WEBSOCKET_PORT=8082
NODE_ENV=production

# Evolution Engine Configuration
MUTATION_RATE=0.01
EVOLUTION_INTERVAL=5000
MAX_ORGANISMS=100
```

### Frontend Environment (.env)
```bash
REACT_APP_BACKEND_URL=https://your-backend-url
REACT_APP_WEBSOCKET_PORT=8082
```

## 📁 Project Structure

```
├── backend/
│   ├── agents/                  # AI agents
│   │   ├── biography_agent.js
│   │   ├── cloud_architect_agent.js
│   │   └── meta_cognition_agent.js
│   ├── lib/                     # Core libraries
│   │   ├── event_bus.js         # Event system
│   │   ├── agent_manager.js     # Agent orchestration
│   │   └── cloud_provisioner.js # Infrastructure automation
│   ├── index.js                 # Main server
│   ├── evolution_engine.js      # Evolution system
│   ├── main.tf                  # Terraform configuration
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── OrganismView.tsx
│   │   │   ├── LineageView.tsx
│   │   │   ├── MarketplaceView.tsx
│   │   │   └── MetricsView.tsx
│   │   ├── services/
│   │   │   └── WebSocketService.ts
│   │   ├── App.tsx
│   │   └── App.css
│   └── package.json
└── .github/workflows/           # CI/CD automation
    └── deploy_terraform.yml
```

## 🎮 Usage Examples

### Trigger Manual Mutation
```javascript
// Via WebSocket
ws.send(JSON.stringify({
  type: 'trigger_mutation',
  organismId: 'organism_123'
}));

// Via REST API
POST /api/organisms/organism_123/mutate
```

### Activate Agents
```javascript
// Activate cloud architect agent
ws.send(JSON.stringify({
  type: 'activate_agent',
  agentType: 'cloud_architect'
}));
```

### Monitor Evolution Events
```javascript
// Listen for real-time events
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch(data.category) {
    case 'evolution':
      console.log('Evolution event:', data);
      break;
    case 'marketplace':
      console.log('Marketplace activity:', data);
      break;
    case 'cloud':
      console.log('Infrastructure update:', data);
      break;
  }
};
```

## 🔧 Extending the System

### Adding New Organism Types
1. Update `generateTraits()` in `evolution_engine.js`
2. Add type-specific genes and behaviors
3. Update frontend organism type colors and icons

### Creating Custom Agents
1. Create new agent file in `backend/agents/`
2. Register agent in `agent_manager.js`
3. Implement agent-specific behaviors and capabilities

### Adding New Visualizations
1. Create new React component in `frontend/src/components/`
2. Add to main navigation in `App.tsx`
3. Style with DNA-Lang theme in `App.css`

## 🚨 Troubleshooting

### Backend Won't Start
- Check that all environment variables are set
- Ensure no other process is using ports 8081/8082
- Verify Node.js version (requires Node 18+)

### Frontend Connection Issues  
- Confirm backend is running and accessible
- Check WebSocket URL in frontend environment
- Verify CORS configuration if accessing from different domain

### Cloud Deployment Issues
- Ensure GCP credentials are properly configured
- Check that required APIs are enabled
- Verify Terraform state and resource quotas

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the live system logs for debugging information

## 🎉 Live Demo

Experience the DNA-Lang Live Digital Ecosystem in action:
- **Dashboard**: Watch organisms evolve in real-time
- **Lineage Tree**: Explore evolutionary relationships  
- **Marketplace**: See gene trading and agent activity
- **Metrics**: Monitor ecosystem health and statistics

The system runs continuously, creating a living digital world where evolution never stops!
