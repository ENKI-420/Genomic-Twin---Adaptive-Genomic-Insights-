# DNA-Lang Examples

This directory contains real-world examples of DNA-Lang organisms demonstrating different use cases and complexity levels.

## Example Organisms

### 🔍 [SimpleMonitor.dna](SimpleMonitor.dna) - Beginner Level

**Use Case**: Basic system monitoring and alerting

A perfect starting point for learning DNA-Lang. This organism demonstrates:
- Simple trigger conditions and mutations
- Basic agent coordination
- Alert management and threshold optimization
- Progressive learning from monitoring data

**Key Features**:
- CPU, memory, and disk monitoring
- Slack, email, and PagerDuty alerts
- Automatic threshold adjustment based on false positive rates
- Resource optimization during low usage periods

**Consciousness Target**: 0.70 (Basic adaptive behavior)

```bash
# Deploy this example
npm run deploy examples/SimpleMonitor.dna
```

### 🌐 [WebScaler.dna](WebScaler.dna) - Intermediate Level

**Use Case**: Autonomous web infrastructure scaling

Demonstrates advanced scaling logic and cost optimization:
- Multi-metric trigger conditions
- Safety-checked infrastructure changes
- Cost control and budget management
- Security-aware scaling decisions

**Key Features**:
- Auto-scaling based on traffic patterns
- Cost optimization without performance degradation
- Security enhancement during scaling events
- Integration with Google Cloud monitoring

**Consciousness Target**: 0.85 (Strategic planning capabilities)

```bash
# Deploy this example
npm run deploy examples/WebScaler.dna
```

### 🧬 [GenomicAnalyzer.dna](GenomicAnalyzer.dna) - Advanced Level

**Use Case**: Autonomous genomic data analysis

Shows complex domain-specific behavior and compliance requirements:
- Advanced bioinformatics algorithms
- HIPAA/GDPR compliance automation
- Population genetics analysis
- Federated learning across research institutions

**Key Features**:
- Variant detection with adaptive accuracy improvement
- Population-scale genomic association studies
- Privacy-preserving analysis techniques
- Computational resource auto-scaling for large datasets

**Consciousness Target**: 0.92 (Near-human level reasoning)

```bash
# Deploy this example (requires genomics data access)
npm run deploy examples/GenomicAnalyzer.dna --environment research
```

### 💊 [DrugDiscoveryPipeline.dna](DrugDiscoveryPipeline.dna) - Expert Level

**Use Case**: Pharmaceutical research automation

Demonstrates the most complex DNA-Lang capabilities:
- Multi-stage drug discovery pipeline
- AI-driven molecular design
- Clinical trial outcome prediction
- Intellectual property management

**Key Features**:
- Target identification using protein interaction networks
- Generative AI for molecular design
- Virtual screening of millions of compounds
- Predictive modeling for clinical success

**Consciousness Target**: 0.88 (Expert-level decision making)

```bash
# Deploy this example (requires pharmaceutical data licenses)
npm run deploy examples/DrugDiscoveryPipeline.dna --environment pharma
```

## Quick Start Guide

### 1. Choose Your Starting Point

- **New to DNA-Lang?** Start with `SimpleMonitor.dna`
- **Web Development Background?** Try `WebScaler.dna`
- **Bioinformatics Experience?** Jump to `GenomicAnalyzer.dna`
- **Pharmaceutical Research?** Explore `DrugDiscoveryPipeline.dna`

### 2. Customize for Your Environment

Each example includes customization points:

```dna
# Modify consciousness target based on your needs
DNA {
  consciousness_target: 0.75  # Adjust based on complexity requirements
}

# Update trigger conditions for your metrics
trigger_conditions: [
  {metric: "your_custom_metric", operator: ">", value: 0.8}
]

# Configure agents for your infrastructure
AGENTS {
  your_agent: YourAgentType(
    custom_parameter: "your_value"
  )
}
```

### 3. Deploy and Monitor

```bash
# Deploy your customized organism
npm run deploy examples/your-organism.dna

# Monitor evolution in real-time
npm run monitor your-organism-id

# View evolution dashboard
open http://localhost:8501
```

## Understanding the Examples

### Complexity Progression

The examples are designed to show increasing complexity:

1. **SimpleMonitor**: Basic mutations, simple agents, single domain
2. **WebScaler**: Multi-gene organisms, safety checks, cost optimization
3. **GenomicAnalyzer**: Domain expertise, compliance, federated operations
4. **DrugDiscoveryPipeline**: Multi-stage pipelines, AI integration, complex workflows

### Common Patterns

#### Trigger Condition Patterns

```dna
# Single threshold
{metric: "cpu_usage", operator: ">", value: 0.8}

# Multiple conditions (AND logic)
trigger_conditions: [
  {metric: "cpu_usage", operator: ">", value: 0.8},
  {metric: "memory_usage", operator: ">", value: 0.7}
]

# Time-based conditions
{metric: "uptime_hours", operator: ">", value: 24}

# Rate-based conditions
{metric: "error_rate", operator: ">", value: 0.01}
```

#### Safety Level Guidelines

```dna
# Basic: Low-risk operations (logging, alerting)
safety_level: "basic"

# Medium: Moderate-risk operations (resource scaling)
safety_level: "medium"  

# High: High-risk operations (infrastructure changes)
safety_level: "high"

# Maximum: Critical operations (data migrations, security changes)
safety_level: "maximum"
```

#### Agent Configuration Patterns

```dna
# Monitoring agents
monitoring_agent: MonitoringAgent(
  interval: "30s",           # Collection frequency
  metrics: ["cpu", "memory"], # Metrics to collect
  retention: "7d"            # Data retention period
)

# Action agents
action_agent: ActionAgent(
  rate_limit: "10/hour",     # Rate limiting
  retry_attempts: 3,         # Retry logic
  timeout: "30s"             # Operation timeout
)

# Analysis agents
analysis_agent: AnalysisAgent(
  window_size: "1h",         # Analysis window
  algorithm: "linear_regression", # Analysis method
  confidence_threshold: 0.8   # Minimum confidence
)
```

## Best Practices Demonstrated

### 1. Safety-First Design

All examples demonstrate:
- Appropriate safety levels for different operations
- Rollback strategies for failed mutations
- Safety checks before executing mutations

### 2. Progressive Complexity

- Start with simple trigger conditions
- Add complexity gradually as consciousness increases
- Use appropriate agent configurations for the domain

### 3. Domain-Specific Optimization

- **Monitoring**: Focus on accuracy and false positive reduction
- **Web Scaling**: Emphasize performance and cost optimization
- **Genomics**: Prioritize privacy and regulatory compliance
- **Pharmaceuticals**: Balance innovation with safety and IP protection

## Customization Guide

### Adding New Mutations

```dna
GENE YourGene {
  purpose: "Description of what this gene does"
  expression_level: 1.0
  
  MUTATIONS {
    yourMutation {
      trigger_conditions: [
        {metric: "your_metric", operator: ">", value: threshold}
      ]
      methods: ["your_method_1", "your_method_2"]
      safety_level: "appropriate_level"
      rollback_strategy: "your_strategy"
      safety_check: "your_validation_function"
    }
  }
}
```

### Adding Custom Agents

```dna
AGENTS {
  your_agent: CustomAgent(
    parameter1: "value1",
    parameter2: 42,
    parameter3: true
  )
}
```

### Environment-Specific Configuration

```dna
# Development environment
DNA {
  security_level: "basic"
  evolution_rate: "fast"      # Quick iteration
  consciousness_target: 0.6   # Lower complexity
}

# Production environment  
DNA {
  security_level: "high"
  evolution_rate: "adaptive"  # Careful evolution
  consciousness_target: 0.85  # Higher intelligence
}
```

## Testing Your Organisms

### Unit Testing

```bash
# Validate DNA syntax
npm run validate examples/YourOrganism.dna

# Test trigger conditions
npm run test-triggers examples/YourOrganism.dna

# Simulate evolution cycles
npm run simulate examples/YourOrganism.dna --cycles 10
```

### Integration Testing

```bash
# Deploy to staging environment
npm run deploy examples/YourOrganism.dna --environment staging

# Run integration tests
npm run test-integration your-organism-id

# Performance testing
npm run test-performance your-organism-id --duration 1h
```

## Contributing Examples

We welcome contributions of new examples! Please:

1. **Follow naming convention**: `YourUseCase.dna`
2. **Include comprehensive documentation**: Purpose, features, setup instructions
3. **Add appropriate metadata**: JSON metadata block at the end
4. **Test thoroughly**: Ensure your example works in multiple environments
5. **Submit a pull request**: Include tests and documentation updates

### Example Template

```dna
# --- Organism: YourOrganismName ---
# Brief description of what this organism does
# Created: YYYY-MM-DD | Domain: your_domain

ORGANISM YourOrganismName
{
  DNA {
    domain: "your_domain"
    security_level: "appropriate_level"
    evolution_rate: "adaptive"
    immune_system: "enabled"
    consciousness_target: 0.XX
  }

  GENOME {
    # Your genes here
  }

  AGENTS {
    # Your agents here
  }
}

# Organism Metadata (JSON):
# {"name":"YourOrganismName","created_at":"YYYY-MM-DDTHH:MM:SSZ","domain":"your_domain",...}
```

## Support

For help with examples:

- **Documentation**: [docs.dnalang.dev/examples](https://docs.dnalang.dev/examples)
- **Community Forum**: [community.dnalang.dev](https://community.dnalang.dev)
- **GitHub Issues**: [Report issues or request examples](https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/issues)
- **Example Requests**: [examples@dnalang.dev](mailto:examples@dnalang.dev)