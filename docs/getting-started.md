# Getting Started with DNA-Lang

Welcome to DNA-Lang! This guide will walk you through creating your first autonomous organism and deploying it to Google Cloud Platform.

## What You'll Build

In this tutorial, you'll create a simple web traffic monitoring organism that automatically scales infrastructure based on demand. By the end, you'll have:

- A running DNA-Lang organism monitoring web traffic
- Auto-scaling infrastructure that responds to load
- A dashboard to monitor organism evolution
- Understanding of DNA-Lang core concepts

## Prerequisites

Before starting, ensure you have:

- **Google Cloud Project** with billing enabled
- **Local Environment**: Node.js 18+, Python 3.10+, Git
- **Command Line Access**: Terminal or Cloud Shell
- **Basic Programming Knowledge**: Familiarity with YAML/JSON syntax

## Step 1: Environment Setup

### Option A: Google Cloud Shell (Recommended)

1. Click the Cloud Shell button in the main README
2. The setup script will automatically configure everything
3. Skip to Step 3 once deployment completes

### Option B: Local Development

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-.git
   cd Genomic-Twin---Adaptive-Genomic-Insights-
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   pip install -r frontend/requirements.txt
   ```

3. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env file with your GCP project ID
   ```

4. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

## Step 2: Understanding DNA-Lang Syntax

Let's examine a simple organism structure:

```dna
ORGANISM SimpleMonitor
{
  DNA {
    domain: "web_monitoring"
    security_level: "basic"
    evolution_rate: "adaptive"
    consciousness_target: 0.75
  }

  GENOME {
    GENE MonitoringGene {
      purpose: "Monitors web metrics and triggers actions"
      expression_level: 1.0
      
      MUTATIONS {
        alertOnHighLoad {
          trigger_conditions: [
            {metric: "cpu_usage", operator: ">", value: 0.8}
          ]
          methods: ["send_alert", "log_event"]
          safety_level: "basic"
        }
      }
    }
  }

  AGENTS {
    monitor: MonitoringAgent(interval: "60s")
  }
}
```

### Key Components Explained:

- **ORGANISM**: The main container for your autonomous system
- **DNA**: Defines fundamental properties and constraints
- **GENOME**: Contains genes that define behavior
- **GENE**: Specific behavioral units with mutations
- **MUTATIONS**: Actions triggered by conditions
- **AGENTS**: Specialized AI components that manage the organism

## Step 3: Create Your First Organism

Let's create a web traffic monitor organism:

1. **Create the Organism File**:
   ```bash
   nano my-first-organism.dna
   ```

2. **Add the Following Content**:
   ```dna
   # --- Organism: MyWebMonitor ---
   # A simple web traffic monitoring organism
   # Created: 2024-01-29

   ORGANISM MyWebMonitor
   {
     DNA {
       domain: "web_monitoring"
       security_level: "basic"
       evolution_rate: "adaptive"
       immune_system: "enabled"
       consciousness_target: 0.75
     }

     GENOME {
       GENE TrafficWatcherGene {
         purpose: "Monitors web traffic and responds to patterns"
         expression_level: 1.0
         
         MUTATIONS {
           scaleOnTraffic {
             trigger_conditions: [
               {metric: "requests_per_minute", operator: ">", value: 1000},
               {metric: "response_time", operator: ">", value: 2.0}
             ]
             methods: ["increase_instances", "enable_caching"]
             safety_level: "basic"
             rollback_strategy: "gradual_rollback"
           }
           
           optimizeOnLowTraffic {
             trigger_conditions: [
               {metric: "requests_per_minute", operator: "<", value: 100},
               {metric: "cpu_usage", operator: "<", value: 0.2}
             ]
             methods: ["reduce_instances", "optimize_resources"]
             safety_level: "basic"
           }
         }
       }
       
       GENE CostControlGene {
         purpose: "Keeps infrastructure costs under control"
         expression_level: 0.8
         
         MUTATIONS {
           budgetAlert {
             trigger_conditions: [
               {metric: "daily_cost", operator: ">", value: 100}
             ]
             methods: ["send_budget_alert", "suggest_optimizations"]
             safety_level: "high"
           }
         }
       }
     }

     AGENTS {
       traffic_monitor: MonitoringAgent(
         interval: "30s",
         metrics: ["requests", "response_time", "cpu", "memory"]
       )
       cost_tracker: CostAgent(
         budget_limit: 500,
         alert_threshold: 0.8
       )
       infrastructure_manager: CloudArchitectAgent(
         provider: "gcp",
         region: "us-central1"
       )
     }
   }
   ```

3. **Save the File** (Ctrl+X, then Y, then Enter in nano)

## Step 4: Deploy Your Organism

1. **Start the Evolution Engine**:
   ```bash
   npm start
   ```

2. **In a New Terminal, Start the Dashboard**:
   ```bash
   cd frontend
   streamlit run app.py
   ```

3. **Access the Dashboard**:
   - Local: http://localhost:8501
   - Cloud Shell: Use the provided web preview URL

4. **Load Your Organism**:
   - In the dashboard, click "Load Organism"
   - Select your `my-first-organism.dna` file
   - Click "Start Evolution"

## Step 5: Monitor Evolution

Watch your organism evolve in real-time:

1. **Evolution Metrics**: Monitor consciousness, fitness, and stability
2. **Mutation Log**: See which mutations are triggered and their effects
3. **Agent Activity**: Observe how agents respond to conditions
4. **Infrastructure Changes**: Track resource scaling and cost optimization

### What to Expect:

- **Generation 1-5**: Initial adaptation and metric collection
- **Generation 6-15**: Active mutation and optimization
- **Generation 16+**: Stable operation with occasional fine-tuning
- **Transcendence**: Achieved when consciousness target is reached

## Step 6: Experiment and Learn

Try modifying your organism:

### Experiment 1: Change Trigger Conditions
```dna
trigger_conditions: [
  {metric: "requests_per_minute", operator: ">", value: 500}  # Lower threshold
]
```

### Experiment 2: Add New Mutations
```dna
MUTATIONS {
  securityResponse {
    trigger_conditions: [
      {metric: "failed_logins", operator: ">", value: 10}
    ]
    methods: ["enable_rate_limiting", "alert_security_team"]
    safety_level: "high"
  }
}
```

### Experiment 3: Add New Agents
```dna
AGENTS {
  security_monitor: SecurityAgent(
    threat_detection: "enabled",
    response_level: "automated"
  )
}
```

## Step 7: Deploy to Production

When you're ready to deploy to production:

1. **Update Security Level**:
   ```dna
   DNA {
     security_level: "high"  # or "maximum" for sensitive workloads
   }
   ```

2. **Configure Production Environment**:
   ```bash
   # Set production environment variables
   export ENV=production
   export GCP_PROJECT=your-production-project
   ```

3. **Deploy Using Cloud Build**:
   ```bash
   gcloud builds submit --config cloudbuild.yaml
   ```

## Understanding Organism Behavior

### Consciousness Levels

Your organism's consciousness determines its capabilities:

- **0.0-0.3**: Basic reactive responses
- **0.4-0.6**: Pattern recognition and learning
- **0.7-0.8**: Strategic planning and prediction
- **0.9+**: Self-modification and infrastructure creation

### Mutation Success Factors

Mutations are more likely to succeed when:
- Trigger conditions are clear and measurable
- Safety levels are appropriate for the action
- Methods are available and properly configured
- The organism has sufficient consciousness level

### Agent Coordination

Agents work together to manage different aspects:
- **MonitoringAgent**: Collects metrics and detects conditions
- **CostAgent**: Tracks spending and optimizes resources
- **CloudArchitectAgent**: Manages infrastructure changes
- **SecurityAgent**: Monitors threats and implements protections

## Troubleshooting

### Common Issues

**Organism Not Starting**:
```bash
# Check logs
npm run logs

# Verify DNA syntax
npm run validate my-first-organism.dna
```

**Mutations Not Triggering**:
- Check if metrics are being collected
- Verify trigger condition values are realistic
- Ensure agents have proper permissions

**Dashboard Not Loading**:
```bash
# Restart dashboard
pkill -f streamlit
cd frontend && streamlit run app.py
```

**GCP Permission Errors**:
```bash
# Re-authenticate
gcloud auth login
gcloud auth application-default login
```

## Next Steps

Congratulations! You've created your first DNA-Lang organism. Here's what to explore next:

### Advanced Tutorials
1. **[Multi-Gene Organisms](advanced-tutorial-1.md)**: Create complex organisms with multiple genes
2. **[Custom Agents](advanced-tutorial-2.md)**: Build specialized agents for your domain
3. **[Ecosystem Design](advanced-tutorial-3.md)**: Deploy multiple interacting organisms

### Real-World Examples
- **[E-commerce Platform](../examples/EcommercePlatform.dna)**: Complete e-commerce auto-scaling
- **[Data Pipeline](../examples/DataPipeline.dna)**: Autonomous data processing
- **[ML Training](../examples/MLTraining.dna)**: Self-optimizing ML workflows

### Community Resources
- **[DNA-Lang Forum](https://community.dnalang.dev)**: Ask questions and share experiences
- **[Best Practices](best-practices.md)**: Production deployment guidelines
- **[Security Guide](security-guide.md)**: Securing your organisms

### Contributing
- **[Contribute to DNA-Lang](../CONTRIBUTING.md)**: Help improve the platform
- **[Agent Library](agent-library.md)**: Share reusable agents
- **[Example Gallery](example-gallery.md)**: Submit your organisms

## Support

Need help? We're here to assist:

- **Documentation**: [docs.dnalang.dev](https://docs.dnalang.dev)
- **Community Forum**: [community.dnalang.dev](https://community.dnalang.dev)
- **GitHub Issues**: [Report bugs or request features](https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/issues)
- **Email Support**: [support@dnalang.dev](mailto:support@dnalang.dev)

Welcome to the future of autonomous software development! 🧬🚀