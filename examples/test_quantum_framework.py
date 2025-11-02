#!/usr/bin/env python3
"""
Unit tests for DNA-Lang Quantum Framework

Simple tests to validate the core functionality of the quantum modules.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import RealAmplitudes, EfficientSU2
from qiskit.transpiler import CouplingMap
from qiskit.quantum_info import SparsePauliOp

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
)


def test_qwc_pass_manager():
    """Test QWC PassManager construction and transpilation."""
    print("Testing QWC PassManager...")
    
    # Create a simple circuit
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    
    # Define hardware constraints
    coupling_map = CouplingMap([(0, 1), (1, 2)])
    basis_gates = ['cx', 'id', 'rz', 'sx', 'x']
    
    # Test PassManager building
    pm = build_qwc_pass_manager(coupling_map, basis_gates)
    assert pm is not None, "PassManager should not be None"
    
    # Test transpilation
    transpiled_qc = transpile_with_qwc(qc, coupling_map, basis_gates)
    assert transpiled_qc is not None, "Transpiled circuit should not be None"
    
    # Test circuit cost analysis
    cost = analyze_circuit_cost(transpiled_qc)
    assert 'two_qubit_gates' in cost, "Cost should include two_qubit_gates"
    assert 'circuit_depth' in cost, "Cost should include circuit_depth"
    
    print("✓ QWC PassManager tests passed")


def test_barren_plateau_diagnostics():
    """Test Barren Plateau diagnostic functionality."""
    print("Testing Barren Plateau diagnostics...")
    
    # Create a simple VQC
    vqc = RealAmplitudes(num_qubits=2, reps=1)
    observable = SparsePauliOp.from_list([("ZZ", 1.0)])
    
    # Test diagnosis with minimal samples
    result = diagnose_barren_plateau(
        circuit=vqc,
        observable=observable,
        num_samples=5,
        seed=42,
    )
    
    assert 'has_barren_plateau' in result, "Result should include has_barren_plateau"
    assert 'gradient_variance' in result, "Result should include gradient_variance"
    assert 'recommendation' in result, "Result should include recommendation"
    assert result['num_parameters'] == vqc.num_parameters
    
    print("✓ Barren Plateau diagnostic tests passed")


def test_fidelity_benchmarking():
    """Test fidelity benchmarking functionality."""
    print("Testing fidelity benchmarking...")
    
    # Create a simple circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    
    observable = SparsePauliOp.from_list([("ZZ", 1.0)])
    
    # Test QWC target calculation
    target_cost = calculate_qwc_target_cost(qc, observable)
    assert isinstance(target_cost, (int, float)), "Target cost should be numeric"
    
    # Test comprehensive benchmarking (noiseless only)
    results = benchmark_circuit_fidelity(qc, observable, backend=None)
    assert 'qwc_target_cost' in results, "Results should include qwc_target_cost"
    assert results['qwc_target_cost'] == target_cost
    
    print("✓ Fidelity benchmarking tests passed")


def test_optimizer_feedback_api():
    """Test optimizer feedback API functionality."""
    print("Testing optimizer feedback API...")
    
    # Create API with constraint
    feedback_api = OptimizerFeedbackAPI(
        constraint=FidelityConstraint(
            mode=OptimizationMode.PENALTY,
            penalty_weight=0.5,
        )
    )
    
    # Test objective computation
    cost = 1.0
    fidelity_dev = 0.1
    params = np.array([0.5, 0.3])
    
    objective = feedback_api.compute_objective(cost, fidelity_dev, params)
    assert isinstance(objective, (int, float)), "Objective should be numeric"
    
    # Test state tracking
    assert feedback_api.state.iteration == 1, "Iteration should be 1 after one call"
    assert len(feedback_api.state.cost_history) == 1
    assert len(feedback_api.state.fidelity_history) == 1
    
    # Test summary
    summary = feedback_api.get_optimization_summary()
    assert 'iterations' in summary
    assert 'avg_fidelity' in summary
    
    print("✓ Optimizer feedback API tests passed")


def test_full_pipeline():
    """Test complete pipeline integration."""
    print("Testing full pipeline integration...")
    
    # Create VQC and decompose it to standard gates first
    vqc = EfficientSU2(num_qubits=2, reps=1)
    vqc = vqc.decompose()  # Decompose to standard gates
    
    coupling_map = CouplingMap([(0, 1)])
    basis_gates = ['cx', 'id', 'rz', 'sx', 'x']
    
    # Step 1: Transpile
    transpiled_vqc = transpile_with_qwc(vqc, coupling_map, basis_gates)
    assert transpiled_vqc is not None
    
    # Step 2: Check Barren Plateau
    observable = SparsePauliOp.from_list([("ZZ", 1.0)])
    bp_result = diagnose_barren_plateau(vqc, observable, num_samples=3, seed=42)
    assert 'has_barren_plateau' in bp_result
    
    # Step 3: Benchmark fidelity
    # Bind parameters for benchmarking
    param_values = {p: 0.1 for p in transpiled_vqc.parameters}
    fidelity_result = benchmark_circuit_fidelity(
        transpiled_vqc, observable, backend=None, parameters=param_values
    )
    assert 'qwc_target_cost' in fidelity_result
    
    # Step 4: Setup feedback
    feedback_api = OptimizerFeedbackAPI()
    assert feedback_api is not None
    
    print("✓ Full pipeline integration tests passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("  DNA-Lang Quantum Framework Unit Tests")
    print("=" * 70 + "\n")
    
    tests = [
        test_qwc_pass_manager,
        test_barren_plateau_diagnostics,
        test_fidelity_benchmarking,
        test_optimizer_feedback_api,
        test_full_pipeline,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"  Test Results: {passed} passed, {failed} failed")
    print("=" * 70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
