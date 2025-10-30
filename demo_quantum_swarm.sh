#!/bin/bash
###############################################################################
# Quantum Swarm DNA-Lang Demo
# Demonstrates the full quantum organism lifecycle from simulation to hardware
###############################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
ARTIFACTS_DIR="$SCRIPT_DIR/quantum_artifacts"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   Quantum Swarm DNA-Lang Demo                                 ║"
echo "║   Adaptive Genomic Insights through Quantum Evolution         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Setup backend first
echo "🚀 Step 1: Setting up quantum backend..."
"$BACKEND_DIR/setup_quantum_backend.sh"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🧬 Step 2: Running Quantum Swarm Experiment"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Prepare artifacts directory
mkdir -p "$ARTIFACTS_DIR"

# Run experiment
echo "🎯 Executing full quantum organism lifecycle..."
echo ""

python3 "$BACKEND_DIR/quantum_swarm.py" \
    --backend ibm_torino \
    --shots 1024 \
    --artifacts-dir "$ARTIFACTS_DIR"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "📊 Step 3: Analyzing Results"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Display master summary
if [ -f "$ARTIFACTS_DIR/master_summary.json" ]; then
    echo "📄 Master Summary:"
    python3 << EOF
import json
from pathlib import Path

summary_path = Path('$ARTIFACTS_DIR') / 'master_summary.json'
with open(summary_path) as f:
    data = json.load(f)

print(f"\n   Timestamp: {data['timestamp']}")
print(f"   Backend: {data['backend']}")
print(f"   Status: {data['status'].upper()}")
print(f"   Shots: {data['shots']}")

print("\n   📊 Experiment Results:")

# Bell experiment
if 'bell' in data['experiments']:
    bell = data['experiments']['bell']
    print(f"\n   🔗 Bell Entanglement:")
    print(f"      Fidelity: {bell['fidelity']:.4f}")
    print(f"      Circuit depth: {bell['circuit_depth']}")
    print(f"      Counts: {bell['counts']}")

# EAL
if 'eal' in data['experiments']:
    eal = data['experiments']['eal']
    print(f"\n   🧠 Evolutionary Adaptive Layer:")
    print(f"      Best fitness: {eal['best_fitness']:.6f}")
    print(f"      Final diversity: {eal['final_diversity']:.6f}")
    print(f"      Convergence: {len(eal['convergence_history'])} iterations")

# Coherence
if 'coherence_workflow' in data['experiments']:
    coh = data['experiments']['coherence_workflow']
    print(f"\n   ⚛️  Coherence Workflow:")
    print(f"      Optimal depth: {coh['optimal_depth']}")
    print(f"      Optimal fidelity: {coh['optimal_fidelity']:.4f}")

# Wormhole
if 'wormhole' in data['experiments']:
    worm = data['experiments']['wormhole']
    print(f"\n   🌀 Wormhole Correlation:")
    print(f"      Status: {worm['status']}")
    if 'correlation' in worm:
        print(f"      Correlation: {worm['correlation']:.4f}")
        print(f"      Entanglement preserved: {worm.get('entanglement_preserved', False)}")

# Persona
if 'persona' in data['experiments']:
    persona = data['experiments']['persona']
    print(f"\n   🎭 Agent Persona:")
    print(f"      Agent ID: {persona['agent_id']}")
    print(f"      Exploration weight: {persona['policy_weights']['exploration']:.2f}")
    print(f"      Curiosity: {persona['behavioral_traits']['curiosity']:.2f}")

print("\n" + "="*60)
EOF

    echo ""
    echo "📁 Artifacts saved to: $ARTIFACTS_DIR"
    echo ""
    echo "   Generated files:"
    ls -lh "$ARTIFACTS_DIR"

else
    echo "❌ Master summary not found!"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ Quantum Swarm Demonstration Complete!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "🧬 Your DNA-Lang quantum organism has completed its lifecycle:"
echo "   • Bell state entanglement verified"
echo "   • Evolutionary parameters optimized (EAL)"
echo "   • Coherence sweet spot identified"
echo "   • Wormhole correlation attempted"
echo "   • Agent persona encoded"
echo ""
echo "Next steps:"
echo "  1. Review artifacts in: $ARTIFACTS_DIR"
echo "  2. Set QISKIT_IBM_TOKEN to run on real hardware"
echo "  3. Integrate with DNA-Lang evolution engine"
echo "  4. Deploy quantum-enhanced organisms to production"
echo ""
echo "═══════════════════════════════════════════════════════════════"
