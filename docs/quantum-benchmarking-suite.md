# Quantum Benchmarking Suite Documentation

## Overview

The **BenchmarkingSuite** organism is a specialized DNA-Lang component that measures the fitness of quantum algorithms generated through evolutionary breeding. It acts as the environmental selection pressure in the quantum algorithm evolutionary cycle, ensuring only the fittest algorithms survive and propagate.

## Purpose

In quantum algorithm evolution, we need an objective way to evaluate and compare different algorithm implementations. The BenchmarkingSuite provides:

1. **Standardized Testing**: Consistent evaluation across all quantum packages
2. **Multi-Dimensional Fitness**: Evaluates algorithms on fidelity, speed, and resource efficiency
3. **Evolutionary Guidance**: Provides clear selection criteria for breeding
4. **Performance Tracking**: Maintains historical metrics for trend analysis

## Architecture

### DNA Configuration

```dna
DNA {
    domain: "quantum_benchmarking_suite"
    target_backend: "simulated_torino_32q"  // Quantum backend
    shots_per_test: 4096                     // Circuit runs per test
    
    // Fitness weights (must sum to 1.0)
    fidelity_weight: 0.50    // Correctness importance
    speed_weight: 0.30       // Execution speed importance
    resource_weight: 0.20    // Resource efficiency importance
}
```

### Genome Structure

The benchmarking suite maintains three critical genes:

#### 1. `pending_tests`
- **Purpose**: Queue of packages awaiting evaluation
- **Encoding**: `Array[PackageID] -> QUBITS[128]`
- **Mutations**: Automatically enqueues new packages when detected

#### 2. `test_protocols`
- **Purpose**: Expected outcomes and validation criteria
- **Encoding**: `map[PackageID, ProtocolDetails] -> QUBITS[256]`
- **Mutations**: Refines protocols based on accuracy feedback

#### 3. `historical_metrics`
- **Purpose**: Performance database for all tested packages
- **Encoding**: `map[PackageID, Array[RawMetrics]] -> QUBITS[512]`
- **Mutations**: Archives results after each test

## Cellular Fabric Components

### 1. TestRunner Cell

Executes quantum circuits on the target backend.

```dna
FUNCTION runQuantumTest(package_id: PackageID) -> RawMetrics
```

**Metrics Collected:**
- Execution time
- Qubit count
- Gate count
- Circuit depth
- Measurement counts
- Error rate

### 2. FidelityEvaluator Cell

Compares actual results with expected outcomes using Hellinger fidelity.

```dna
FUNCTION evaluateFidelity(metrics: RawMetrics, protocol: ProtocolDetails) -> Float
```

**Formula:**
```
Fidelity = (Σ √(p_i * q_i))² × (1 - error_rate)
```

Where:
- `p_i` = Expected probability for state i
- `q_i` = Actual probability for state i

**Score Range:** 0.0 (complete mismatch) to 1.0 (perfect match)

### 3. SpeedEvaluator Cell

Evaluates execution time against baseline.

```dna
FUNCTION evaluateSpeed(metrics: RawMetrics, baseline_time: Float) -> Float
```

**Formula:**
```
Speed Score = {
    1.0                      if execution_time ≤ baseline_time
    baseline_time / execution_time    otherwise
}
```

**Score Range:** 0.0 (very slow) to 1.0 (at or above baseline)

### 4. ResourceEvaluator Cell

Assesses quantum resource usage efficiency.

```dna
FUNCTION evaluateResources(metrics: RawMetrics, max_resources: ResourceLimits) -> Float
```

**Formula:**
```
Resource Score = (
    (1 - qubits/max_qubits) +
    (1 - gates/max_gates) +
    (1 - depth/max_depth)
) / 3
```

**Score Range:** 0.0 (maximum resources) to 1.0 (minimal resources)

### 5. FitnessCalculator Cell

Computes weighted final fitness score.

```dna
FUNCTION calculateFitnessScore(fidelity, speed, resources) -> FitnessScore
```

**Formula:**
```
Total Fitness = 
    (fidelity × fidelity_weight) +
    (speed × speed_weight) +
    (resources × resource_weight)
```

**Output:**
```javascript
{
    total: 0.0-1.0,
    fidelity_component: weighted value,
    speed_component: weighted value,
    resource_component: weighted value,
    raw_fidelity: unweighted score,
    raw_speed: unweighted score,
    raw_resources: unweighted score
}
```

### 6. BenchmarkOrchestrator Cell

Main orchestration logic that coordinates all other cells.

```dna
FUNCTION processBenchmarkQueue() -> void
```

**Workflow:**
1. Read pending tests from queue
2. For each package:
   - Run quantum test
   - Evaluate fidelity
   - Evaluate speed
   - Evaluate resources
   - Calculate final fitness
   - Store results in historical metrics
3. Clear processed queue

## Usage Examples

### Example 1: Testing Grover's Algorithm

```dna
// Setup test protocol
protocol = {
    package_id: "grover_search_v1",
    expected_distribution: {
        "101": 0.65,  // Target state
        // ... other states with low probability
    },
    baseline_time: 2.5,
    resource_limits: {
        max_qubits: 10,
        max_gates: 100,
        max_depth: 50
    }
}

// Add to queue
INVOKE BenchmarkingSuite.GENOME.pending_tests.addTestToQueue("grover_search_v1")

// Register protocol
INVOKE BenchmarkingSuite.GENOME.test_protocols.updateProtocol("grover_search_v1", protocol)

// Trigger benchmark
INVOKE BenchmarkingSuite.LIFECYCLE.ON_EVOLUTION()

// Retrieve results
results = READ BenchmarkingSuite.GENOME.historical_metrics["grover_search_v1"]
```

### Example 2: Evolutionary Selection

```dna
// Get fitness score
fitness = results.fitness.total

// Make breeding decision
IF fitness >= 0.85 {
    decision = "PROMOTE_TO_PRODUCTION"
} ELSE IF fitness >= 0.70 {
    decision = "BREED_FOR_IMPROVEMENT"
} ELSE IF fitness >= 0.50 {
    decision = "CONTINUE_EVOLUTION"
} ELSE {
    decision = "DISCARD"
}
```

## Fitness Interpretation Guide

| Fitness Score | Quality | Action |
|--------------|---------|--------|
| 0.85 - 1.00 | Excellent | Promote to production, use as breeding parent |
| 0.70 - 0.84 | Good | Include in breeding pool |
| 0.50 - 0.69 | Acceptable | Continue evolution, apply mutations |
| 0.00 - 0.49 | Poor | Discard from population |

## Configuration Guidelines

### Adjusting Fitness Weights

**For Correctness-Critical Applications:**
```dna
fidelity_weight: 0.70
speed_weight: 0.20
resource_weight: 0.10
```

**For Speed-Critical Applications:**
```dna
fidelity_weight: 0.40
speed_weight: 0.50
resource_weight: 0.10
```

**For Resource-Constrained Environments:**
```dna
fidelity_weight: 0.40
speed_weight: 0.20
resource_weight: 0.40
```

### Choosing Shots Per Test

| Shots | Use Case | Accuracy | Time |
|-------|----------|----------|------|
| 1024 | Rapid screening | Lower | Fast |
| 4096 | Standard testing | Good | Moderate |
| 8192 | High precision | Better | Slow |
| 16384+ | Critical validation | Best | Very slow |

## Integration with Evolution Engine

The BenchmarkingSuite integrates seamlessly with DNA-Lang's evolution engine:

```bash
# Compile the benchmarking suite
dna compile BenchmarkingSuite.dna --optimize --target=production

# Evolve with benchmarking
dna evolve QuantumAlgorithm --optimize-for=fitness --generations=100
```

During evolution, the suite automatically:
1. Evaluates each new algorithm variant
2. Assigns fitness scores
3. Guides parent selection for breeding
4. Tracks performance trends

## Advanced Features

### 1. Historical Trend Analysis

```dna
// Get all historical data
all_results = READ BenchmarkingSuite.GENOME.historical_metrics

// Calculate trends
FOR package_id, results IN all_results {
    trend = CALCULATE_TREND(results)
    IF trend == "improving" {
        PRINT "Package ${package_id} is evolving successfully"
    }
}
```

### 2. Custom Evaluation Metrics

Extend the suite with custom evaluators:

```dna
CELL CustomEvaluator {
    FUNCTION evaluateCustomMetric(metrics: RawMetrics) -> Float {
        // Your custom evaluation logic
        RETURN custom_score
    }
}
```

### 3. Multi-Backend Testing

Test across different quantum backends:

```dna
backends = ["simulated_torino_32q", "ibm_perth", "ionq_harmony"]

FOR backend IN backends {
    DNA.target_backend = backend
    BenchmarkOrchestrator.processBenchmarkQueue()
}
```

## Performance Considerations

### Benchmarking Time

Approximate time per test:
- Circuit execution: 1-10 seconds
- Evaluation: < 0.1 seconds
- Total per package: ~2-15 seconds

For large populations (100+ algorithms), consider:
- Parallel testing on multiple backends
- Incremental benchmarking
- Caching of stable algorithms

### Resource Requirements

- **Memory**: ~100MB per 1000 historical records
- **Quantum Backend**: Access to IBM Quantum, IonQ, or simulator
- **CPU**: Minimal (evaluation is lightweight)

## Troubleshooting

### Common Issues

**1. Fitness weights don't sum to 1.0**
```
Error: Fitness weights must sum to 1.0
Solution: Adjust weights in DNA configuration
```

**2. Backend connection failed**
```
Error: Cannot connect to quantum backend
Solution: Verify backend name and credentials
```

**3. Protocol mismatch**
```
Error: No protocol found for package_id
Solution: Register protocol before adding to queue
```

## API Reference

### Key Functions

```dna
// Add package to test queue
addTestToQueue(package_id: String)

// Update test protocol
updateProtocol(package_id: String, protocol: ProtocolDetails)

// Retrieve results
getHistoricalMetrics(package_id: String) -> ResultData

// Process all queued tests
processBenchmarkQueue()
```

### Data Structures

```javascript
RawMetrics = {
    package_id: String,
    execution_time: Float,
    qubit_count: Int,
    gate_count: Int,
    circuit_depth: Int,
    measurement_counts: Map[String, Int],
    error_rate: Float,
    timestamp: DateTime
}

FitnessScore = {
    total: Float,
    fidelity_component: Float,
    speed_component: Float,
    resource_component: Float,
    raw_fidelity: Float,
    raw_speed: Float,
    raw_resources: Float
}

ProtocolDetails = {
    expected_distribution: Map[String, Float],
    baseline_time: Float,
    resource_limits: ResourceLimits
}

ResourceLimits = {
    max_qubits: Int,
    max_gates: Int,
    max_depth: Int
}
```

## See Also

- [Quantum Algorithm Evolution Guide](./quantum-evolution-guide.md)
- [DNA-Lang Language Reference](./language-reference.md)
- [Example: Quantum Benchmark Workflow](../examples/QuantumBenchmarkExample.dna)

## Contributing

To extend the BenchmarkingSuite:

1. Add new evaluation cells for custom metrics
2. Implement additional backend support
3. Create specialized protocols for different algorithm types
4. Contribute analysis tools for historical data

## License

MIT License - See LICENSE file for details
