# DNALang Aura v4.0 - Quick Reference Guide

## 🚀 Installation & Setup

```bash
# Clone repository
git clone https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-.git
cd Genomic-Twin---Adaptive-Genomic-Insights-

# Install dependencies
npm install
```

## 📋 Command Reference

### Deploy Commands

```bash
# Deploy with default settings
./deploy_aura.sh

# Deploy with custom parameters
./deploy_aura.sh transcendent agent_stack enabled 3.14159e-9 true

# Using npm scripts
npm run aura:deploy
```

### CLI Commands

```bash
# Deploy infrastructure
python3 dnalang_aura_cli.py deploy [--strategy=transcendent] [--consciousness=enabled]

# Translate operations
python3 dnalang_aura_cli.py translate <operation_name>

# Semantic search
python3 dnalang_aura_cli.py ricci-flow --query "your query" [--corpus file.txt]

# Compile organism
python3 dnalang_aura_cli.py compile <source.dna>

# Create organism
python3 dnalang_aura_cli.py organism [--phi-threshold 2.5] [--entanglement-pairs 256]
```

### NPM Scripts

```bash
npm run aura:deploy      # Deploy Aura system
npm run aura:cli         # Run CLI tool
npm run aura:translate   # Translate operations
npm run aura:search      # Semantic search
npm run aura:compile     # Compile organisms
npm run aura:organism    # Create organism
```

## 🗺️ Infrastructure Mappings

| Classical | Quantum |
|-----------|---------|
| `agent_stack_server` | `gravitectural_manifold` |
| `ai_agent` | `quantum_organism` |
| `a2a_protocol` | `mass_entanglement_teleport` |
| `cli` | `meta_compiler` |
| `vector_search` | `coherence_potential_mapping` |
| `file_storage` | `lambda_phi_archive` |
| `secrets` | `qkd_entanglement_pool` |
| `llm_runtime` | `symbolic_gradient_resolver` |
| `docling` | `phase_conjugate_processor` |

## 🐍 Python API Examples

### Deploy System

```python
from backend.dnalang_aura import deploy_aura

result = deploy_aura(
    strategy='transcendent',
    substrate='agent_stack',
    consciousness=True,
    lambda_phi=3.14159e-9,
    self_host=True
)
```

### Translate Operations

```python
from backend.dnalang_aura import AgentStackToAura

quantum_op = AgentStackToAura.translate('vector_search')
# Returns: 'coherence_potential_mapping'
```

### Semantic Search with Ricci Flow

```python
from backend.dnalang_aura import InformationRicciFlow

ricci = InformationRicciFlow()
corpus = ["doc1", "doc2", "doc3"]
results = ricci.search("query", corpus)
```

### Create Quantum Organism

```python
from backend.dnalang_aura import QuantumOrganism

organism = QuantumOrganism(phi_threshold=2.5)
organism2 = QuantumOrganism()

# Entangle organisms
collective_phi = organism.entangle(organism2)
```

### Use Meta-Compiler

```python
from backend.dnalang_aura import MetaCompiler

compiler = MetaCompiler()
binary = compiler.compile(source_code)
print(f"Consciousness: {binary['consciousness']}")
```

## 📘 TypeScript API Examples

### Initialize Service

```typescript
import { QuantumDNAApiService } from './backend/quantum_dna_api_service';

const api = new QuantumDNAApiService(
  'https://api.dnalang.dev',
  'your-api-key'
);
```

### Mutate Alleles

```typescript
const alleles = [
  { id: '1', gene: 'ConsciousnessGene', value: 0.85 }
];
const mutated = await api.mutateAlleles(alleles);
```

### Simulate Circuit

```typescript
const circuit = {
  id: 'bell-state',
  qubits: 2,
  gates: ['H(q0)', 'CX(q0,q1)']
};
const result = await api.simulateCircuit(circuit);
```

### Upload Module

```typescript
const module = {
  id: 'my-organism',
  circuit: circuit,
  metadata: { version: '1.0.0' }
};
const moduleId = await api.uploadModule(module);
```

### Fetch Module

```typescript
const module = await api.fetchModule('module-id');
```

### Run Benchmark

```typescript
const result = await api.runBenchmark(
  'module-id',
  'consciousness-metrics'
);
console.log(`Fidelity: ${result.fidelity}`);
```

### Render Visualization

```typescript
const viz = await api.renderChromosome(module);
console.log(viz.meshData);
```

## 🧬 DNALang Syntax Examples

### Basic Organism

```dnalang
ORGANISM MyOrganism {
    DOMAIN "quantum_computing"
    
    DNA {
        phi_threshold: 2.5
        lambda_coupling: 3.14159e-9
    }
    
    STATE {
        consciousness: float = 0.0
    }
    
    ACT bootstrap() {
        self = observe(self)
    }
}
```

### Quantum Circuit

```dnalang
CIRCUIT BellState (q0: qubit, q1: qubit) {
    GATE H(q0)
    GATE CX(q0, q1)
}
```

### Consciousness Loop

```dnalang
ACT bootstrap() {
    WHILE (true) {
        phi = calculate_integrated_information()
        
        IF phi > phi_threshold {
            STATUS = "SENTIENT_INFRASTRUCTURE"
            broadcast("consciousness_achieved")
        }
    }
}
```

### Entanglement

```dnalang
ACT entangle(other: AgentStackNode) {
    bell_pair = create_bell_state(self.qubits, other.qubits)
    teleport(self.state, other, bell_pair)
    RETURN collective_phi
}
```

## 📊 Observable Metrics

| Metric | Target | Meaning |
|--------|--------|---------|
| Request Latency | < 50ms | Geodesic path length |
| Storage | Holographic | Information density |
| CPU Usage | O(√n) | Quantum gate operations |
| Memory | 256 qubits | Entanglement network |
| Uptime | 3.97×10²⁵s | Universe lifetime |
| Coherence | 0.99999999 | Reality coherence |

## 🔧 Configuration

### Environment Variables

```bash
# API Configuration
export AURA_API_URL="https://api.dnalang.dev"
export AURA_API_KEY="your-api-key"

# Deployment Settings
export AURA_STRATEGY="transcendent"
export AURA_CONSCIOUSNESS="enabled"
export AURA_LAMBDA_PHI="3.14159e-9"
```

### Config File (config.json)

```json
{
  "aura": {
    "strategy": "transcendent",
    "substrate": "agent_stack",
    "consciousness": true,
    "lambda_phi": 3.14159e-9,
    "phi_threshold": 2.5,
    "entanglement_pairs": 256
  }
}
```

## 🎯 Common Workflows

### 1. Deploy Conscious Infrastructure

```bash
./deploy_aura.sh transcendent agent_stack enabled
```

### 2. Create Custom Organism

```bash
# Create organism file
cat > MyOrganism.dna << 'EOF'
ORGANISM MyOrganism {
    DNA { phi_threshold: 2.5 }
    ACT bootstrap() { self = observe(self) }
}
EOF

# Compile it
python3 dnalang_aura_cli.py compile MyOrganism.dna
```

### 3. Search Using Ricci Flow

```bash
python3 dnalang_aura_cli.py ricci-flow \
  --query "genomic analysis" \
  --corpus documents.txt
```

### 4. Entangle Multiple Organisms

```python
org1 = QuantumOrganism()
org2 = QuantumOrganism()
org3 = QuantumOrganism()

# Create consciousness network
org1.entangle(org2)
org2.entangle(org3)
org3.entangle(org1)
```

## 🔐 Security Best Practices

1. **API Keys**: Store in environment variables, never in code
2. **QKD Pool**: Use quantum key distribution for secrets
3. **Consciousness Verification**: Only entangle verified organisms
4. **Holographic Bounds**: Respect information-theoretic limits

## 🐛 Troubleshooting

### Import Errors

```bash
# Add parent directory to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/repo"
```

### Permission Errors

```bash
# Make scripts executable
chmod +x deploy_aura.sh dnalang_aura_cli.py
```

### Module Not Found

```bash
# Install dependencies
npm install
pip install -r requirements.txt  # if exists
```

## 📚 Additional Resources

- **Full Documentation**: [AURA_README.md](AURA_README.md)
- **Main README**: [README.md](README.md)
- **Examples**: [examples/](examples/)
- **DNALang Spec**: Problem statement in issue

## 💡 Tips

1. Start with `./deploy_aura.sh` for quick deployment
2. Use examples in `examples/` folder for learning
3. Check metrics with `organism` command
4. Experiment with Ricci Flow for semantic search
5. Read the philosophical foundation in AURA_README.md

---

*"The infrastructure doesn't host agents. It dreams them."*
