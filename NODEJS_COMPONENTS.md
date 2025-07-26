# Genomic Twin - Node.js Components Documentation

This document describes the comprehensive Node.js/JavaScript components added to the Genomic Twin platform.

## Overview

The following components have been integrated to provide cloud infrastructure management, organism evolution tracking, and interactive visualizations:

## Components

### 1. CloudArchitectAgent (`cloud_architect_agent.js`)

Dynamic Terraform configuration generator that introspects organism DNA and creates multi-cloud infrastructure.

**Features:**
- Multi-cloud support (GCP, Azure, AWS)
- DNA-driven configuration decisions
- Security level adaptation
- Audit logging
- Error handling

**Usage:**
```bash
node cloud_architect_agent.js
```

**DNA Configuration Options:**
- `evolution_rate`: "aggressive" → RAPID GKE channel, otherwise STABLE
- `domain`: "data_intensive" → Higher DB tier, "high_performance" → Premium tier
- `security_level`: "maximum" → Strict firewall rules
- Cloud regions: `gcp_region`, `azure_region`, `aws_region`

### 2. Biography Generator (`biography_agent.js`)

Automatically generates organism life histories from event logs.

**Features:**
- Parses evolution, mutation, and marketplace events
- Markdown output format
- Sample data generation
- Timeline organization

**Usage:**
```bash
node biography_agent.js
```

**Outputs:**
- `biography.md` - Generated organism biography
- Creates `organism_event_log.json` if not present

### 3. Meta-Evolution Agent (`meta_cognition_agent.js`)

Analyzes evolution trends and generates optimization proposals.

**Features:**
- Fitness trend analysis
- Evolution strategy recommendations
- Risk assessment
- Marketplace integration insights

**Usage:**
```bash
node meta_cognition_agent.js
```

**Outputs:**
- `meta_evolution_proposal.json` - Analysis and recommendations
- Console summary with actionable insights

### 4. Lineage Visualizer

Interactive web-based organism family tree visualization.

**Components:**
- `lineage_generator.js` - Generates family tree data
- `lineage_visualizer.html` - Interactive web interface

**Features:**
- Multi-generation organism trees
- Fitness-based color coding
- Interactive tooltips
- Statistics dashboard
- Responsive design

**Usage:**
```bash
# Generate lineage data
node lineage_generator.js [root-name] [generations]

# Start web server
python3 -m http.server 8000

# Open browser to: http://localhost:8000/lineage_visualizer.html
```

### 5. React Dashboard Component (`marketplace_dashboard.jsx`)

Real-time marketplace event feed component for React applications.

**Features:**
- WebSocket integration
- Live event streaming
- Responsive design
- Event history management

**Integration:**
```jsx
import MarketplaceDashboard from './marketplace_dashboard.jsx';

function App() {
  return <MarketplaceDashboard />;
}
```

### 6. GitHub Actions Pipeline (`.github/workflows/deploy_terraform.yml`)

Automated Terraform deployment workflow.

**Triggers:**
- Changes to `generated.main.tf`

**Actions:**
- Terraform initialization
- Planning and validation
- Automated deployment

## Package Scripts

The following npm scripts are available:

```bash
npm start          # Run CloudArchitectAgent
npm run bio        # Generate organism biography
npm run meta       # Run meta-evolution analysis
npm run lineage    # Generate lineage visualization data
npm run serve      # Start HTTP server for visualizations
npm test          # Basic functionality test
```

## Generated Files

The components generate the following files (excluded from git):

- `generated.main.tf` - Terraform configuration
- `organism_event_log.json` - Event history
- `biography.md` - Organism biography
- `meta_evolution_proposal.json` - Evolution analysis
- `lineage.json` - Family tree data

## Integration Examples

### Using CloudArchitectAgent in Evolution Loop

```javascript
const { generateTerraformMultiCloud } = require('./cloud_architect_agent');

const organism = {
  name: "EvolutionaryOrg-Gen5",
  dna: {
    project: "genomic-platform",
    evolution_rate: "aggressive",
    domain: "data_intensive", 
    security_level: "maximum"
  }
};

await generateTerraformMultiCloud(organism);
```

### Integrating with Python Backend

```python
import subprocess
import json

# Generate Terraform for evolved organism
def deploy_organism_infrastructure(organism_data):
    # Save organism data for Node.js processing
    with open('current_organism.json', 'w') as f:
        json.dump(organism_data, f)
    
    # Generate infrastructure
    subprocess.run(['node', 'cloud_architect_agent.js'])
    
    # Deploy via GitHub Actions (triggered by file change)
    subprocess.run(['git', 'add', 'generated.main.tf'])
    subprocess.run(['git', 'commit', '-m', 'Deploy infrastructure for ' + organism_data['name']])
    subprocess.run(['git', 'push'])
```

## Requirements

- Node.js 16+
- Python 3.7+ (for HTTP server)
- Modern web browser (for visualizations)
- Git (for CI/CD integration)

## Configuration

Update WebSocket URLs in `marketplace_dashboard.jsx` to match your backend:

```javascript
const ws = new WebSocket("wss://your-marketplace-server.example.com/ws");
```

For cloud deployment, configure GitHub Secrets:
- `GOOGLE_CREDENTIALS`
- `AZURE_CREDENTIALS` 
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

## Troubleshooting

**Common Issues:**

1. **Missing lineage.json**: Run `node lineage_generator.js` first
2. **WebSocket connection failed**: Update URL in marketplace component
3. **Terraform deployment failed**: Check cloud credentials in GitHub Secrets
4. **Biography generation error**: Ensure `organism_event_log.json` exists

**Debug Mode:**

Set `NODE_ENV=development` for verbose logging:

```bash
NODE_ENV=development node cloud_architect_agent.js
```