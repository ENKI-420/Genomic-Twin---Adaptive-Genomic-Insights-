# DNA-Lang Language Reference

DNA-Lang is a domain-specific language for creating autonomous bio-digital organisms. This reference covers the complete syntax and semantics of the language.

## Basic Syntax

### Organism Declaration

Every DNA-Lang program defines an organism:

```dna
ORGANISM OrganismName
{
  // Organism definition
}
```

### DNA Block

The DNA block defines the fundamental properties of the organism:

```dna
DNA {
  domain: "string"              // Application domain
  security_level: "level"       // none, basic, high, maximum
  evolution_rate: "rate"        // static, slow, adaptive, fast
  immune_system: "boolean"      // enabled, disabled
  consciousness_target: float   // 0.0 to 1.0
}
```

### Genome Structure

The genome contains genes that define the organism's behavior:

```dna
GENOME {
  GENE GeneName {
    purpose: "description"
    expression_level: float     // 0.0 to 1.0
    
    MUTATIONS {
      mutationName {
        trigger_conditions: [
          {metric: "name", operator: "op", value: number}
        ]
        methods: ["method1", "method2"]
        safety_level: "level"
        rollback_strategy: "strategy"
      }
    }
  }
}
```

### Agent System

Organisms can employ specialized agents:

```dna
AGENTS {
  agent_name: AgentType(param: value)
}
```

## Data Types

### Primitive Types

- **string**: Text values enclosed in quotes
- **float**: Floating-point numbers (0.0 to 1.0 for percentages)
- **boolean**: true/false or "enabled"/"disabled"
- **array**: Lists of values `[item1, item2, item3]`

### Complex Types

- **metric_condition**: `{metric: "name", operator: "comparison", value: number}`
- **agent_specification**: `AgentType(parameter: value, ...)`

## Operators

### Comparison Operators

- `<`: Less than
- `<=`: Less than or equal
- `>`: Greater than
- `>=`: Greater than or equal
- `==`: Equal to
- `!=`: Not equal to

## Built-in Agent Types

### ConsciousnessAgent
Monitors and manages consciousness levels.

```dna
consciousness_monitor: ConsciousnessAgent(
  depth: shallow|deep,
  sensitivity: low|medium|high
)
```

### LearningAgent
Optimizes learning and adaptation processes.

```dna
learning_optimizer: LearningAgent(
  strategy: static|adaptive|dynamic,
  rate: slow|medium|fast
)
```

### MetaAnalysisAgent
Performs meta-cognitive analysis.

```dna
meta_analyzer: MetaAnalysisAgent(
  scope: local|global,
  analysis_depth: basic|advanced|expert
)
```

### CloudArchitectAgent
Manages cloud infrastructure provisioning.

```dna
cloud_architect: CloudArchitectAgent(
  provider: gcp|aws|azure,
  scale: small|medium|large|auto
)
```

## Standard Mutation Methods

### Consciousness Mutations
- `increaseIntrospection`: Enhances self-awareness
- `enhanceMetaCognition`: Improves meta-cognitive abilities
- `expandAwareness`: Broadens consciousness scope

### Learning Mutations
- `adjustLearningRate`: Modifies learning speed
- `refinePatterns`: Improves pattern recognition
- `optimizeMemory`: Enhances memory efficiency

### Infrastructure Mutations
- `generate_terraform_for_gcp`: Creates GCP infrastructure
- `scale_resources`: Adjusts resource allocation
- `optimize_performance`: Improves system performance

## Security Levels

- **none**: No security restrictions
- **basic**: Standard security measures
- **high**: Enhanced security protocols
- **maximum**: Military-grade security

## Evolution Rates

- **static**: No autonomous evolution
- **slow**: Gradual, careful evolution
- **adaptive**: Context-aware evolution
- **fast**: Rapid, aggressive evolution

## Rollback Strategies

- **immediate_rollback**: Instant reversion on failure
- **gradual_rollback**: Step-by-step reversion
- **checkpoint_rollback**: Return to last safe state
- **no_rollback**: No automatic reversion

## Example Program

```dna
# --- Organism: WebScaler ---
# Automatically scales web infrastructure based on traffic

ORGANISM WebScaler
{
  DNA {
    domain: "web_infrastructure"
    security_level: "high"
    evolution_rate: "adaptive"
    immune_system: "enabled"
    consciousness_target: 0.80
  }

  GENOME {
    GENE TrafficMonitorGene {
      purpose: "Monitors web traffic and triggers scaling"
      expression_level: 1.0
      
      MUTATIONS {
        scaleUp {
          trigger_conditions: [
            {metric: "cpu_usage", operator: ">", value: 0.8},
            {metric: "response_time", operator: ">", value: 2.0}
          ]
          methods: ["increase_instances", "add_load_balancer"]
          safety_level: "high"
          rollback_strategy: "gradual_rollback"
        }
        
        scaleDown {
          trigger_conditions: [
            {metric: "cpu_usage", operator: "<", value: 0.3},
            {metric: "traffic", operator: "<", value: 0.1}
          ]
          methods: ["reduce_instances", "optimize_resources"]
          rollback_strategy: "checkpoint_rollback"
        }
      }
    }
  }

  AGENTS {
    traffic_monitor: MonitoringAgent(interval: "30s")
    infrastructure_manager: CloudArchitectAgent(provider: "gcp")
    cost_optimizer: CostAgent(budget: "aggressive")
  }
}
```

## Comments

Comments in DNA-Lang start with `#`:

```dna
# This is a single-line comment
ORGANISM Example  # End-of-line comment
{
  # Comments can appear anywhere
  DNA {
    domain: "example"  # Inline comments are supported
  }
}
```

## Best Practices

1. **Use descriptive names**: Make gene and mutation names self-explanatory
2. **Set appropriate safety levels**: Higher levels for production systems
3. **Define clear trigger conditions**: Avoid ambiguous or conflicting conditions
4. **Include rollback strategies**: Always plan for failure scenarios
5. **Monitor consciousness levels**: Keep targets realistic for your domain
6. **Document purposes**: Every gene should have a clear purpose statement

## Error Handling

DNA-Lang includes built-in error handling through:

- **Safety checks**: Automated validation of mutation parameters
- **Rollback mechanisms**: Automatic reversion on failure
- **Immune system**: Protection against harmful mutations
- **Agent supervision**: Multi-agent monitoring and correction

## Integration Points

DNA-Lang organisms can integrate with:

- **Google Cloud Platform**: Native GCP resource management
- **Terraform**: Infrastructure as Code generation
- **Kubernetes**: Container orchestration
- **Monitoring systems**: Prometheus, Grafana, Cloud Monitoring
- **CI/CD pipelines**: GitHub Actions, Cloud Build