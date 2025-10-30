"""
Barren Plateau Diagnostics for Variational Quantum Circuits (VQC)

This module implements the Gradient Variance Method for detecting
Barren Plateaus in VQC optimization landscapes. A vanishing gradient
variance indicates a Barren Plateau that will prevent successful
optimization.

Mathematical Background:
    A Barren Plateau is characterized by:
    Var[∂L/∂θ] ∝ exp(-poly(N))
    
    For a trainable landscape, we expect:
    Var[∂L/∂θ] ∝ 1/poly(N)
"""

import numpy as np
from typing import List, Dict, Optional, Callable
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.primitives import Estimator
from qiskit.quantum_info import SparsePauliOp


def diagnose_barren_plateau(
    circuit: QuantumCircuit,
    observable: SparsePauliOp,
    num_samples: int = 50,
    epsilon: float = np.pi / 2,
    variance_threshold: float = 1e-6,
    seed: Optional[int] = None,
) -> Dict[str, any]:
    """
    Diagnose potential Barren Plateau in a parameterized quantum circuit.

    Uses the Parameter Shift Rule to compute gradients and analyze their
    variance across the parameter landscape. A vanishing variance indicates
    a Barren Plateau.

    Args:
        circuit: Parameterized quantum circuit (VQC)
        observable: Observable to measure (e.g., Hamiltonian for VQE)
        num_samples: Number of random parameter configurations to sample
        epsilon: Shift value for parameter shift rule (default: π/2)
        variance_threshold: Threshold below which landscape is considered barren
        seed: Random seed for reproducibility

    Returns:
        Dictionary containing:
        - 'has_barren_plateau': bool indicating if BP detected
        - 'gradient_variance': mean variance of gradients
        - 'gradient_samples': list of gradient variances per sample
        - 'variance_threshold': threshold used
        - 'num_parameters': number of circuit parameters
        - 'recommendation': string with recommendation

    Example:
        >>> from qiskit.circuit.library import RealAmplitudes
        >>> from qiskit.quantum_info import SparsePauliOp
        >>> 
        >>> # Create a VQC
        >>> qc = RealAmplitudes(num_qubits=4, reps=2)
        >>> observable = SparsePauliOp.from_list([("ZZZZ", 1.0)])
        >>> 
        >>> # Diagnose Barren Plateau
        >>> result = diagnose_barren_plateau(qc, observable, num_samples=30)
        >>> print(f"Barren Plateau detected: {result['has_barren_plateau']}")
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Get circuit parameters
    parameters = list(circuit.parameters)
    num_params = len(parameters)
    
    if num_params == 0:
        return {
            'has_barren_plateau': False,
            'gradient_variance': None,
            'gradient_samples': [],
            'variance_threshold': variance_threshold,
            'num_parameters': 0,
            'recommendation': 'Circuit has no parameters - not applicable',
        }
    
    # Initialize estimator for noiseless simulation
    estimator = Estimator()
    
    # Sample gradient variances
    gradient_variances = []
    
    for sample_idx in range(num_samples):
        # Sample random parameter values
        param_values = np.random.uniform(-np.pi, np.pi, num_params)
        
        # Compute gradients for each parameter using parameter shift rule
        gradients = []
        for param_idx, param in enumerate(parameters):
            # Parameter shift: evaluate at θ + ε and θ - ε
            param_dict_plus = {p: param_values[i] for i, p in enumerate(parameters)}
            param_dict_minus = {p: param_values[i] for i, p in enumerate(parameters)}
            
            param_dict_plus[param] = param_values[param_idx] + epsilon
            param_dict_minus[param] = param_values[param_idx] - epsilon
            
            # Bind parameters
            circuit_plus = circuit.assign_parameters(param_dict_plus)
            circuit_minus = circuit.assign_parameters(param_dict_minus)
            
            # Compute expectation values
            job = estimator.run([circuit_plus, circuit_minus], [observable, observable])
            result = job.result()
            
            exp_plus = result.values[0]
            exp_minus = result.values[1]
            
            # Gradient via parameter shift rule
            gradient = (exp_plus - exp_minus) / (2 * np.sin(epsilon))
            gradients.append(gradient)
        
        # Compute variance of gradients for this sample
        grad_variance = np.var(gradients)
        gradient_variances.append(grad_variance)
    
    # Analyze results
    mean_gradient_variance = np.mean(gradient_variances)
    has_barren_plateau = mean_gradient_variance < variance_threshold
    
    # Generate recommendation
    if has_barren_plateau:
        recommendation = (
            f"⚠️ BARREN PLATEAU DETECTED: Mean gradient variance "
            f"({mean_gradient_variance:.2e}) is below threshold "
            f"({variance_threshold:.2e}). Recommendations:\n"
            f"  1. Reduce circuit depth (currently {circuit.depth()} depth)\n"
            f"  2. Use local cost functions instead of global observables\n"
            f"  3. Consider circuit ansatz with better trainability\n"
            f"  4. Apply pre-training or warm-start strategies"
        )
    else:
        recommendation = (
            f"✓ TRAINABLE LANDSCAPE: Mean gradient variance "
            f"({mean_gradient_variance:.2e}) is above threshold. "
            f"Optimization should be tractable."
        )
    
    return {
        'has_barren_plateau': has_barren_plateau,
        'gradient_variance': mean_gradient_variance,
        'gradient_samples': gradient_variances,
        'variance_threshold': variance_threshold,
        'num_parameters': num_params,
        'num_samples': num_samples,
        'recommendation': recommendation,
    }


def compute_gradient_variance_scaling(
    circuit_template: Callable[[int], QuantumCircuit],
    observable_template: Callable[[int], SparsePauliOp],
    qubit_range: List[int],
    num_samples: int = 20,
    seed: Optional[int] = None,
) -> Dict[str, any]:
    """
    Analyze gradient variance scaling with system size.

    Computes how gradient variance scales with the number of qubits,
    which helps identify exponential vs polynomial decay characteristic
    of Barren Plateaus.

    Args:
        circuit_template: Function that creates circuit given num_qubits
        observable_template: Function that creates observable given num_qubits
        qubit_range: List of qubit numbers to test
        num_samples: Number of samples per qubit count
        seed: Random seed for reproducibility

    Returns:
        Dictionary containing scaling analysis results

    Example:
        >>> def make_circuit(n):
        ...     return RealAmplitudes(num_qubits=n, reps=2)
        >>> 
        >>> def make_observable(n):
        ...     return SparsePauliOp.from_list([("Z" * n, 1.0)])
        >>> 
        >>> scaling = compute_gradient_variance_scaling(
        ...     make_circuit, make_observable, [2, 4, 6, 8]
        ... )
    """
    results = {
        'qubit_counts': [],
        'gradient_variances': [],
        'has_exponential_decay': False,
        'scaling_analysis': '',
    }
    
    variances_by_qubits = []
    
    for num_qubits in qubit_range:
        circuit = circuit_template(num_qubits)
        observable = observable_template(num_qubits)
        
        diagnosis = diagnose_barren_plateau(
            circuit=circuit,
            observable=observable,
            num_samples=num_samples,
            seed=seed,
        )
        
        results['qubit_counts'].append(num_qubits)
        results['gradient_variances'].append(diagnosis['gradient_variance'])
        variances_by_qubits.append((num_qubits, diagnosis['gradient_variance']))
    
    # Analyze scaling
    if len(variances_by_qubits) >= 2:
        # Check if variance decays exponentially
        # Exponential: Var ∝ exp(-aN) → log(Var) ∝ -aN
        log_variances = np.log([v for _, v in variances_by_qubits])
        qubits = np.array([n for n, _ in variances_by_qubits])
        
        # Fit linear model to log-variance vs qubits
        coeffs = np.polyfit(qubits, log_variances, 1)
        slope = coeffs[0]
        
        # Negative slope indicates exponential decay
        if slope < -0.1:  # Threshold for significant exponential decay
            results['has_exponential_decay'] = True
            results['scaling_analysis'] = (
                f"⚠️ EXPONENTIAL DECAY DETECTED: Gradient variance scales as "
                f"exp({slope:.3f}·N), indicating Barren Plateau. "
                f"Circuit is likely untrainable at scale."
            )
        else:
            results['scaling_analysis'] = (
                f"✓ POLYNOMIAL SCALING: Gradient variance has polynomial or "
                f"sub-exponential decay (slope: {slope:.3f}). "
                f"Circuit maintains trainability with scale."
            )
    
    return results
