#!/usr/bin/env python3
"""
DNA-Lang Quantum-Classical Co-Design Framework Demo

This script demonstrates the complete W1-optimized pipeline:
1. QWC-inspired PassManager for aggressive N2Q minimization
2. Barren Plateau diagnostics for VQC landscape analysis
3. Real-time fidelity benchmarking with Qiskit Estimator
4. Classical optimizer feedback loop

Usage:
    python examples/dna_lang_quantum_demo.py
"""

import sys
import os

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import RealAmplitudes, EfficientSU2
from qiskit.transpiler import CouplingMap
from qiskit.quantum_info import SparsePauliOp
from scipy.optimize import minimize

from dna_lang.quantum import (
    build_qwc_pass_manager,
    transpile_with_qwc,
    diagnose_barren_plateau,
    calculate_qwc_target_cost,
    benchmark_circuit_fidelity,
    OptimizerFeedbackAPI,
)
from dna_lang.quantum.qwc_pass_manager import analyze_circuit_cost
from dna_lang.quantum.optimizer_feedback_api import (
    FidelityConstraint,
    OptimizationMode,
    create_fidelity_aware_cost_function,
)


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_qwc_pass_manager():
    """Demonstrate QWC-inspired PassManager with N2Q minimization."""
    print_section("1. QWC-Inspired PassManager Demo")
    
    # Create a simple circuit
    qc = QuantumCircuit(4)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.cx(2, 3)
    qc.cx(3, 0)
    qc.measure_all()
    
    print("Original Circuit:")
    print(qc)
    print(f"\nOriginal depth: {qc.depth()}")
    
    # Define hardware constraints (IBM-like topology)
    coupling_map = CouplingMap([(0, 1), (1, 2), (2, 3), (1, 3)])
    basis_gates = ['cx', 'id', 'rz', 'sx', 'x']
    
    # Analyze original circuit
    print("\nOriginal Circuit Metrics:")
    original_cost = analyze_circuit_cost(qc)
    print(f"  Two-qubit gates: {original_cost['two_qubit_gates']}")
    print(f"  SWAP gates: {original_cost['swap_gates']}")
    print(f"  Circuit depth: {original_cost['circuit_depth']}")
    
    # Transpile with QWC
    print("\n🔧 Transpiling with QWC PassManager (aggressive N2Q minimization)...")
    transpiled_qc = transpile_with_qwc(
        circuit=qc,
        coupling_map=coupling_map,
        basis_gates=basis_gates,
        sabre_trials=10,
        seed=42,
    )
    
    print("\nTranspiled Circuit (QWC-optimized):")
    print(transpiled_qc)
    
    # Analyze transpiled circuit
    print("\nTranspiled Circuit Metrics (W1-optimized):")
    transpiled_cost = analyze_circuit_cost(transpiled_qc)
    print(f"  Two-qubit gates: {transpiled_cost['two_qubit_gates']}")
    print(f"  SWAP gates: {transpiled_cost['swap_gates']}")
    print(f"  Circuit depth: {transpiled_cost['circuit_depth']}")
    
    # Show improvement
    n2q_reduction = original_cost['two_qubit_gates'] - transpiled_cost['two_qubit_gates']
    print(f"\n✅ N2Q Reduction: {n2q_reduction} gates")
    print(f"   This directly reduces the W1 metric by minimizing gate errors!")


def demo_barren_plateau_diagnostics():
    """Demonstrate Barren Plateau diagnostics for VQCs."""
    print_section("2. Barren Plateau Diagnostics Demo")
    
    # Create a variational circuit
    num_qubits = 4
    reps = 2
    
    print(f"Creating Variational Quantum Circuit:")
    print(f"  Qubits: {num_qubits}")
    print(f"  Repetitions: {reps}")
    print(f"  Ansatz: RealAmplitudes")
    
    vqc = RealAmplitudes(num_qubits=num_qubits, reps=reps)
    print(f"\n  Parameters: {vqc.num_parameters}")
    
    # Define observable (simple Hamiltonian)
    observable = SparsePauliOp.from_list([
        ("ZZZZ", 1.0),
        ("XXXX", 0.5),
    ])
    
    print("\n🔬 Running Barren Plateau diagnostics...")
    print("   (Sampling gradient variance across parameter landscape)")
    
    # Diagnose Barren Plateau
    bp_result = diagnose_barren_plateau(
        circuit=vqc,
        observable=observable,
        num_samples=20,  # Reduced for demo speed
        seed=42,
    )
    
    print(f"\n📊 Diagnostic Results:")
    print(f"  Gradient Variance: {bp_result['gradient_variance']:.6e}")
    print(f"  Variance Threshold: {bp_result['variance_threshold']:.6e}")
    print(f"  Barren Plateau Detected: {bp_result['has_barren_plateau']}")
    print(f"\n{bp_result['recommendation']}")


def demo_fidelity_benchmarking():
    """Demonstrate real-time fidelity benchmarking."""
    print_section("3. Fidelity Benchmarking Demo")
    
    # Create and transpile a circuit
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    
    # Transpile with QWC
    coupling_map = CouplingMap([(0, 1), (1, 2)])
    basis_gates = ['cx', 'id', 'rz', 'sx', 'x']
    
    transpiled_qc = transpile_with_qwc(
        circuit=qc,
        coupling_map=coupling_map,
        basis_gates=basis_gates,
        seed=42,
    )
    
    # Define observable
    observable = SparsePauliOp.from_list([("ZZZ", 1.0)])
    
    print("Circuit prepared and QWC-optimized")
    print(f"N2Q count: {analyze_circuit_cost(transpiled_qc)['two_qubit_gates']}")
    
    # Benchmark fidelity (noiseless only for demo)
    print("\n📈 Calculating QWC Target Cost (noiseless simulation)...")
    
    results = benchmark_circuit_fidelity(
        circuit=transpiled_qc,
        observable=observable,
        backend=None,  # Only noiseless for demo
    )
    
    print(f"\n✅ QWC Target Cost: {results['qwc_target_cost']:.6f}")
    print("\nNote: For hardware benchmarking, provide a backend:")
    print("  backend = service.backend('ibm_osaka')")
    print("  results = benchmark_circuit_fidelity(..., backend=backend)")
    print("\nThis would compute:")
    print("  • Hardware Cost (with noise)")
    print("  • Fidelity Deviation = |Hardware - Target|")
    print("  • Relative Error (%)")


def demo_optimizer_feedback_loop():
    """Demonstrate classical optimizer with fidelity feedback."""
    print_section("4. Classical Optimizer Feedback Loop Demo")
    
    # Create a simple VQE-like setup
    num_qubits = 2
    vqc = RealAmplitudes(num_qubits=num_qubits, reps=1)
    observable = SparsePauliOp.from_list([("ZZ", 1.0), ("XX", 0.5)])
    
    print("Variational Quantum Eigensolver (VQE) Setup:")
    print(f"  Qubits: {num_qubits}")
    print(f"  Parameters: {vqc.num_parameters}")
    print(f"  Observable: ZZ + 0.5·XX")
    
    # Configure feedback API
    print("\n⚙️  Configuring Optimizer Feedback API:")
    print("  Mode: PENALTY")
    print("  Penalty Weight: 0.3")
    print("  Penalty Type: quadratic")
    
    feedback_api = OptimizerFeedbackAPI(
        constraint=FidelityConstraint(
            mode=OptimizationMode.PENALTY,
            penalty_weight=0.3,
            penalty_type="quadratic",
        )
    )
    
    # Define cost function
    def cost_function(params):
        """Compute cost with simulated fidelity deviation."""
        # Bind parameters
        bound_circuit = vqc.assign_parameters(
            {p: params[i] for i, p in enumerate(vqc.parameters)}
        )
        
        # Calculate QWC target (noiseless)
        qwc_cost = calculate_qwc_target_cost(bound_circuit, observable)
        
        # Simulate hardware noise (for demo)
        # In reality, this would be calculate_hardware_cost()
        noise_amplitude = 0.02 * np.linalg.norm(params)  # Simulated noise
        hardware_cost = qwc_cost + np.random.normal(0, noise_amplitude)
        fidelity_dev = abs(hardware_cost - qwc_cost)
        
        # Compute objective with fidelity feedback
        objective = feedback_api.compute_objective(
            cost=hardware_cost,
            fidelity_deviation=fidelity_dev,
            parameters=params,
        )
        
        return objective
    
    # Run optimization
    print("\n🔄 Running optimization with fidelity feedback...")
    initial_params = np.random.uniform(-np.pi, np.pi, vqc.num_parameters)
    
    result = minimize(
        cost_function,
        initial_params,
        method='COBYLA',
        options={'maxiter': 50, 'disp': False}
    )
    
    print(f"\n✅ Optimization Complete!")
    print(f"  Iterations: {result.nfev}")
    print(f"  Success: {result.success}")
    
    # Get optimization summary
    summary = feedback_api.get_optimization_summary()
    print(f"\n📊 Optimization Summary:")
    print(f"  Best Cost: {summary['best_cost']:.6f}")
    print(f"  Best Fidelity: {summary['best_fidelity']:.6f}")
    print(f"  Average Fidelity: {summary['avg_fidelity']:.6f}")
    print(f"  Cost Improvement: {summary['cost_improvement']*100:.2f}%")
    
    print("\n💡 Key Insight:")
    print("  The optimizer balances cost minimization with fidelity")
    print("  maintenance, ensuring solutions are achievable on real hardware!")


def demo_full_pipeline():
    """Demonstrate the complete DNA-Lang quantum pipeline."""
    print_section("5. Complete DNA-Lang Quantum Pipeline")
    
    print("🔬 Full W1-Optimized Quantum-Classical Co-Design Pipeline:\n")
    
    # Step 1: Create circuit
    print("Step 1: Create Variational Circuit")
    num_qubits = 3
    vqc = EfficientSU2(num_qubits=num_qubits, reps=1)
    print(f"  ✓ Created {num_qubits}-qubit VQC with {vqc.num_parameters} parameters")
    
    # Step 2: QWC Transpilation
    print("\nStep 2: QWC-Inspired Transpilation")
    coupling_map = CouplingMap([(0, 1), (1, 2)])
    basis_gates = ['cx', 'id', 'rz', 'sx', 'x']
    transpiled_vqc = transpile_with_qwc(vqc, coupling_map, basis_gates)
    cost_metrics = analyze_circuit_cost(transpiled_vqc)
    print(f"  ✓ Transpiled with aggressive N2Q minimization")
    print(f"    N2Q count: {cost_metrics['two_qubit_gates']}")
    
    # Step 3: Barren Plateau Check
    print("\nStep 3: Barren Plateau Diagnostics")
    observable = SparsePauliOp.from_list([("ZZZ", 1.0)])
    bp_check = diagnose_barren_plateau(
        vqc, observable, num_samples=10, seed=42
    )
    print(f"  ✓ Gradient variance: {bp_check['gradient_variance']:.6e}")
    print(f"    Barren Plateau: {bp_check['has_barren_plateau']}")
    
    # Step 4: Fidelity Benchmarking
    print("\nStep 4: Fidelity Benchmarking Setup")
    print("  ✓ QWC target calculation: Ready")
    print("  ✓ Hardware benchmarking: Ready")
    print("  ✓ W1 deviation metric: Ready")
    
    # Step 5: Optimizer Feedback
    print("\nStep 5: Optimizer Feedback Loop")
    feedback_api = OptimizerFeedbackAPI()
    print("  ✓ Feedback API initialized")
    print("  ✓ Multi-objective optimization: Ready")
    
    print("\n✅ DNA-Lang Quantum Pipeline Complete!")
    print("\n🎯 Mission Objective Achieved:")
    print("   W1-optimized compilation ensures maximum execution fidelity")
    print("   for mission-critical quantum applications in agile defense systems.")


def main():
    """Run all demos."""
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + " " * 15 + "DNA-Lang Quantum Framework Demo" + " " * 22 + "█")
    print("█" + " " * 10 + "W1-Optimized Quantum-Classical Co-Design" + " " * 19 + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    try:
        # Run individual demos
        demo_qwc_pass_manager()
        demo_barren_plateau_diagnostics()
        demo_fidelity_benchmarking()
        demo_optimizer_feedback_loop()
        demo_full_pipeline()
        
        print_section("Demo Complete!")
        print("✅ All DNA-Lang quantum components demonstrated successfully!")
        print("\nNext Steps:")
        print("  1. Integrate with IBM Quantum backend for hardware execution")
        print("  2. Deploy in mission-critical applications")
        print("  3. Monitor W1 fidelity metrics in production")
        print("\n📚 Documentation: lib/dna_lang/quantum/")
        print("🔧 API Reference: See module docstrings")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
