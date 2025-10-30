#!/bin/bash
###############################################################################
# Quantum Swarm DNA-Lang Backend Setup
# Sets up IBM Quantum hardware authentication and environment
###############################################################################

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   Quantum Swarm DNA-Lang Backend Setup                        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "📌 Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 is required but not found."
    exit 1
fi
echo "   ✓ Python 3 detected"
echo ""

# Install requirements
echo "📦 Installing quantum computing dependencies..."
pip3 install -r "$SCRIPT_DIR/quantum_requirements.txt" --prefer-binary --quiet
echo "   ✓ Dependencies installed"
echo ""

# Check for IBM Quantum API key
echo "🔑 Checking IBM Quantum authentication..."

if [ -z "$QISKIT_IBM_TOKEN" ]; then
    echo ""
    echo "⚠️  QISKIT_IBM_TOKEN environment variable not set."
    echo ""
    echo "To enable hardware backend execution:"
    echo "  1. Get your API token from: https://quantum.ibm.com/account"
    echo "  2. Set the environment variable:"
    echo "     export QISKIT_IBM_TOKEN='your_token_here'"
    echo ""
    echo "  OR create a .env file in the project root:"
    echo "     echo 'QISKIT_IBM_TOKEN=your_token_here' >> $PROJECT_ROOT/.env"
    echo ""
    echo "  OR provide a JSON file with apikey field:"
    echo "     python3 -c \"import json; print(json.load(open('path/to/apikey.json'))['apikey'])\""
    echo ""
    echo "⚠️  Continuing without hardware authentication (simulator only)..."
else
    echo "   ✓ QISKIT_IBM_TOKEN found"

    # Validate token
    echo "   Validating IBM Quantum credentials..."
    python3 << EOF
try:
    from qiskit_ibm_runtime import QiskitRuntimeService
    service = QiskitRuntimeService(channel='ibm_quantum', token='$QISKIT_IBM_TOKEN')
    backends = service.backends()
    print(f"   ✓ Authentication successful! Available backends: {len(backends)}")

    # List some backends
    print("   Available hardware backends:")
    for backend in list(backends)[:5]:
        print(f"      - {backend.name}")
except Exception as e:
    print(f"   ❌ Authentication failed: {e}")
    exit(1)
EOF
fi

echo ""
echo "🧬 Testing quantum swarm module..."
python3 << EOF
import sys
sys.path.insert(0, '$SCRIPT_DIR')

try:
    from quantum_swarm import QuantumSwarmDNA
    print("   ✓ quantum_swarm module loaded successfully")

    # Quick sanity test
    config = {'backend': 'aer_simulator', 'shots': 100, 'artifacts_dir': '/tmp/test_quantum'}
    swarm = QuantumSwarmDNA(config)
    print(f"   ✓ Backend initialized: {swarm.backend}")

except Exception as e:
    print(f"   ❌ Module test failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
EOF

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ Quantum backend setup complete!"
echo ""
echo "To run a full experiment:"
echo "  python3 $SCRIPT_DIR/quantum_swarm.py --backend ibm_torino --shots 1024"
echo ""
echo "To use custom artifacts directory:"
echo "  python3 $SCRIPT_DIR/quantum_swarm.py --artifacts-dir ./my_results"
echo ""
echo "═══════════════════════════════════════════════════════════════"
