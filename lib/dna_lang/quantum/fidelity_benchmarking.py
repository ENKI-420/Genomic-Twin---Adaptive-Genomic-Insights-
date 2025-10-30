"""
Fidelity Benchmarking with Qiskit Estimator

This module implements real-time QWC fidelity benchmarking using the
Qiskit Estimator primitive. It calculates the W1 fidelity deviation
metric that quantifies the difference between ideal (QWC-optimized)
and hardware execution.

Mathematical Framework:
    Fidelity Deviation = |Cost_Hardware - Cost_QWC_Target|
    
    This serves as an empirical proxy for the W1 distance:
    W1(μ_ideal, μ_noisy)
"""

import numpy as np
from typing import Dict, Optional, List, Union
from qiskit import QuantumCircuit
try:
    from qiskit.primitives import StatevectorEstimator as Estimator
except ImportError:
    from qiskit.primitives import Estimator
from qiskit.quantum_info import SparsePauliOp


def calculate_qwc_target_cost(
    circuit: QuantumCircuit,
    observable: SparsePauliOp,
    parameters: Optional[Dict] = None,
) -> float:
    """
    Calculate the theoretical QWC target cost using noiseless simulation.

    This represents the ideal expectation value that the QWC-optimized
    circuit should achieve in the absence of hardware noise.

    Args:
        circuit: The QWC-optimized quantum circuit
        observable: Observable to measure (e.g., cost Hamiltonian)
        parameters: Optional parameter values for parameterized circuits

    Returns:
        The theoretical QWC target cost (noiseless expectation value)

    Example:
        >>> from qiskit import QuantumCircuit
        >>> from qiskit.quantum_info import SparsePauliOp
        >>> 
        >>> qc = QuantumCircuit(2)
        >>> qc.h(0)
        >>> qc.cx(0, 1)
        >>> 
        >>> observable = SparsePauliOp.from_list([("ZZ", 1.0)])
        >>> target_cost = calculate_qwc_target_cost(qc, observable)
    """
    # Create noiseless estimator
    estimator = Estimator()
    
    # Bind parameters if provided
    if parameters is not None:
        circuit = circuit.assign_parameters(parameters)
    
    # Run noiseless simulation
    try:
        # New API (V2)
        job = estimator.run([(circuit, observable)])
        result = job.result()
        return float(result[0].data.evs)
    except (AttributeError, TypeError, IndexError):
        # Old API (V1) or fallback
        job = estimator.run(circuit, observable)
        result = job.result()
        return result.values[0]


def calculate_hardware_cost(
    circuit: QuantumCircuit,
    observable: SparsePauliOp,
    backend,
    parameters: Optional[Dict] = None,
    shots: int = 1024,
    session_kwargs: Optional[Dict] = None,
) -> float:
    """
    Calculate the hardware cost using a real quantum backend.

    This measures the actual expectation value achieved on the target
    IBM QPU, including all hardware noise effects.

    Args:
        circuit: The QWC-optimized quantum circuit
        observable: Observable to measure
        backend: Qiskit backend (real QPU or noisy simulator)
        parameters: Optional parameter values for parameterized circuits
        shots: Number of measurement shots
        session_kwargs: Optional kwargs for QiskitRuntimeService Session

    Returns:
        The hardware cost (noisy expectation value)

    Example:
        >>> from qiskit_ibm_runtime import QiskitRuntimeService
        >>> 
        >>> service = QiskitRuntimeService()
        >>> backend = service.backend("ibm_osaka")
        >>> 
        >>> hardware_cost = calculate_hardware_cost(
        ...     qc, observable, backend, shots=2048
        ... )

    Note:
        This function requires qiskit-ibm-runtime to be installed
        for real hardware execution. For development/testing, use
        a noisy simulator backend.
    """
    try:
        from qiskit_ibm_runtime import Estimator as RuntimeEstimator, Session
        
        # Bind parameters if provided
        if parameters is not None:
            circuit = circuit.assign_parameters(parameters)
        
        # Execute on hardware with session
        if session_kwargs is None:
            session_kwargs = {}
        
        with Session(backend=backend, **session_kwargs) as session:
            estimator = RuntimeEstimator(session=session)
            job = estimator.run(circuit, observable, shots=shots)
            result = job.result()
            
            return result.values[0]
    
    except ImportError:
        # Fallback to basic Estimator if runtime not available
        # This would typically be a noisy simulator
        from qiskit_aer import AerSimulator
        from qiskit_aer.primitives import Estimator as AerEstimator
        
        # Create noisy simulator if needed
        if hasattr(backend, 'configuration'):
            noisy_sim = AerSimulator.from_backend(backend)
        else:
            noisy_sim = backend
        
        estimator = AerEstimator(backend=noisy_sim)
        
        if parameters is not None:
            circuit = circuit.assign_parameters(parameters)
        
        try:
            # New API (V2)
            job = estimator.run([(circuit, observable)])
            result = job.result()
            return float(result[0].data.evs)
        except (AttributeError, TypeError, IndexError):
            # Old API (V1)
            job = estimator.run(circuit, observable, shots=shots)
            result = job.result()
            return result.values[0]


def calculate_fidelity_deviation(
    qwc_target_cost: float,
    hardware_cost: float,
) -> float:
    """
    Calculate the W1 fidelity deviation metric.

    This metric quantifies the real-world noise impact that the
    QWC-inspired transpiler was unable to mitigate, serving as
    an empirical proxy for the Wasserstein-1 distance.

    Args:
        qwc_target_cost: Theoretical cost from noiseless simulation
        hardware_cost: Actual cost from hardware execution

    Returns:
        Fidelity deviation (absolute difference)

    Mathematical Definition:
        Fidelity Deviation = |Cost_Hardware - Cost_QWC_Target|
        
        This approximates: W1(μ_ideal, μ_noisy)
    """
    return abs(hardware_cost - qwc_target_cost)


def benchmark_circuit_fidelity(
    circuit: QuantumCircuit,
    observable: SparsePauliOp,
    backend=None,
    parameters: Optional[Dict] = None,
    shots: int = 1024,
    session_kwargs: Optional[Dict] = None,
) -> Dict[str, float]:
    """
    Comprehensive fidelity benchmarking for a quantum circuit.

    Computes both QWC target and hardware costs, then calculates
    the fidelity deviation metric. This provides a complete view
    of circuit performance.

    Args:
        circuit: The QWC-optimized quantum circuit
        observable: Observable to measure
        backend: Optional backend for hardware execution (if None, only target is computed)
        parameters: Optional parameter values
        shots: Number of measurement shots for hardware
        session_kwargs: Optional session configuration

    Returns:
        Dictionary containing:
        - 'qwc_target_cost': Theoretical noiseless cost
        - 'hardware_cost': Actual hardware cost (if backend provided)
        - 'fidelity_deviation': W1 proxy metric (if backend provided)
        - 'relative_error': Relative error percentage (if backend provided)

    Example:
        >>> results = benchmark_circuit_fidelity(
        ...     circuit=transpiled_qc,
        ...     observable=hamiltonian,
        ...     backend=backend,
        ...     shots=2048
        ... )
        >>> 
        >>> print(f"Target: {results['qwc_target_cost']:.4f}")
        >>> print(f"Hardware: {results['hardware_cost']:.4f}")
        >>> print(f"Deviation: {results['fidelity_deviation']:.4f}")
    """
    # Calculate QWC target (always computed)
    qwc_target = calculate_qwc_target_cost(circuit, observable, parameters)
    
    results = {
        'qwc_target_cost': qwc_target,
    }
    
    # Calculate hardware cost if backend provided
    if backend is not None:
        hardware_cost = calculate_hardware_cost(
            circuit=circuit,
            observable=observable,
            backend=backend,
            parameters=parameters,
            shots=shots,
            session_kwargs=session_kwargs,
        )
        
        fidelity_dev = calculate_fidelity_deviation(qwc_target, hardware_cost)
        
        results['hardware_cost'] = hardware_cost
        results['fidelity_deviation'] = fidelity_dev
        
        # Compute relative error
        if abs(qwc_target) > 1e-10:
            results['relative_error'] = abs(fidelity_dev / qwc_target) * 100
        else:
            results['relative_error'] = None
    
    return results


def track_fidelity_over_optimization(
    circuit_template: QuantumCircuit,
    observable: SparsePauliOp,
    parameter_history: List[Dict],
    backend=None,
    shots: int = 1024,
) -> Dict[str, List]:
    """
    Track fidelity deviation throughout an optimization process.

    This function benchmarks circuit fidelity at each step of a
    variational optimization, providing insight into how noise
    affects the optimization trajectory.

    Args:
        circuit_template: Parameterized circuit template
        observable: Observable to measure
        parameter_history: List of parameter dictionaries from optimization
        backend: Optional backend for hardware tracking
        shots: Number of shots per evaluation

    Returns:
        Dictionary containing lists of:
        - 'iterations': Iteration numbers
        - 'qwc_target_costs': Target costs per iteration
        - 'hardware_costs': Hardware costs per iteration (if backend provided)
        - 'fidelity_deviations': Deviations per iteration (if backend provided)

    Example:
        >>> # During optimization, save parameters
        >>> param_history = []
        >>> def callback(params):
        ...     param_history.append(params.copy())
        >>> 
        >>> # After optimization, track fidelity
        >>> tracking = track_fidelity_over_optimization(
        ...     circuit, observable, param_history, backend
        ... )
    """
    results = {
        'iterations': list(range(len(parameter_history))),
        'qwc_target_costs': [],
        'hardware_costs': [],
        'fidelity_deviations': [],
    }
    
    for params in parameter_history:
        benchmark = benchmark_circuit_fidelity(
            circuit=circuit_template,
            observable=observable,
            backend=backend,
            parameters=params,
            shots=shots,
        )
        
        results['qwc_target_costs'].append(benchmark['qwc_target_cost'])
        
        if backend is not None:
            results['hardware_costs'].append(benchmark['hardware_cost'])
            results['fidelity_deviations'].append(benchmark['fidelity_deviation'])
    
    return results
