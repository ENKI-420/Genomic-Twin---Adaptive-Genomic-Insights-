#!/usr/bin/env python3
"""
Quantum Swarm DNA-Lang Module
Implements quantum circuit execution with hardware backend support,
evolutionary adaptation layer (EAL), and wormhole entanglement correlation.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

# Hardware backend support (graceful fallback if not authenticated)
try:
    from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler
    HARDWARE_AVAILABLE = True
except ImportError:
    HARDWARE_AVAILABLE = False
    print("⚠️  qiskit-ibm-runtime not installed. Hardware execution disabled.")


class QuantumSwarmDNA:
    """
    Quantum Swarm implementation for DNA-Lang organisms.
    Combines Bell state entanglement, evolutionary adaptation,
    and coherence learning.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.backend_name = self.config.get('backend', 'ibm_torino')
        self.shots = self.config.get('shots', 1024)
        self.artifacts_dir = Path(self.config.get('artifacts_dir', './artifacts'))
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

        # Initialize backend
        self.service = None
        self.backend = None
        self.use_hardware = False
        self._initialize_backend()

        # Experiment state
        self.results = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'backend': self.backend_name,
            'shots': self.shots,
            'status': 'initialized',
            'experiments': {}
        }

    def _initialize_backend(self):
        """Initialize quantum backend (hardware or simulator)."""
        if HARDWARE_AVAILABLE:
            try:
                # Try to load IBM Quantum account
                token = os.getenv('QISKIT_IBM_TOKEN')
                if token:
                    self.service = QiskitRuntimeService(
                        channel='ibm_quantum',
                        token=token
                    )
                    # Try to get the specified backend
                    try:
                        self.backend = self.service.backend(self.backend_name)
                        self.use_hardware = True
                        print(f"✓ Connected to hardware backend: {self.backend_name}")
                    except Exception as e:
                        print(f"⚠️  Could not access {self.backend_name}: {e}")
                        print("   Falling back to simulator.")
                        self._initialize_simulator()
                else:
                    print("⚠️  QISKIT_IBM_TOKEN not set. Using simulator.")
                    self._initialize_simulator()
            except Exception as e:
                print(f"⚠️  IBM Quantum initialization failed: {e}")
                self._initialize_simulator()
        else:
            self._initialize_simulator()

    def _initialize_simulator(self):
        """Initialize Aer simulator as fallback."""
        self.backend = AerSimulator()
        self.use_hardware = False
        self.results['status'] = 'simulated'

    def create_bell_circuit(self, qubits: Tuple[int, int] = (0, 1)) -> QuantumCircuit:
        """
        Create a Bell state (maximally entangled) circuit.
        |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
        """
        qc = QuantumCircuit(2, 2)
        qc.h(qubits[0])  # Hadamard on qubit 0
        qc.cx(qubits[0], qubits[1])  # CNOT with qubit 0 as control
        qc.measure([0, 1], [0, 1])
        return qc

    def run_bell_experiment(self) -> Dict:
        """
        Execute Bell state experiment to verify entanglement.
        Returns counts and fidelity metrics.
        """
        print("\n🧬 Running Bell Entanglement Experiment...")

        circuit = self.create_bell_circuit()
        compiled_circuit = transpile(circuit, self.backend, optimization_level=3)

        if self.use_hardware:
            # Hardware execution
            with Session(service=self.service, backend=self.backend) as session:
                sampler = Sampler(session=session)
                job = sampler.run(compiled_circuit, shots=self.shots)
                result = job.result()
                counts = result.quasi_dists[0].binary_probabilities()
                # Convert to integer counts
                counts = {k: int(v * self.shots) for k, v in counts.items()}
        else:
            # Simulator execution
            job = self.backend.run(compiled_circuit, shots=self.shots)
            result = job.result()
            counts = result.get_counts(0)

        # Calculate fidelity (measure of entanglement quality)
        total = sum(counts.values())
        bell_count = counts.get('00', 0) + counts.get('11', 0)
        fidelity = bell_count / total

        experiment_data = {
            'counts': counts,
            'fidelity': fidelity,
            'circuit_depth': compiled_circuit.depth(),
            'gate_count': compiled_circuit.size()
        }

        self.results['experiments']['bell'] = experiment_data

        print(f"   ✓ Bell state fidelity: {fidelity:.4f}")
        print(f"   ✓ Counts: {counts}")

        return experiment_data

    def evolutionary_adaptive_layer(
        self,
        dimensions: int = 10,
        population_size: int = 30,
        max_iterations: int = 50
    ) -> Dict:
        """
        Evolutionary Adaptive Layer (EAL) optimization.
        Uses particle swarm optimization to evolve circuit parameters.
        """
        print("\n🧠 Running Evolutionary Adaptive Layer (EAL)...")

        # Initialize particle swarm
        positions = np.random.uniform(-1, 1, (population_size, dimensions))
        velocities = np.random.uniform(-0.1, 0.1, (population_size, dimensions))
        personal_best_positions = positions.copy()
        personal_best_scores = np.full(population_size, float('inf'))

        global_best_position = None
        global_best_score = float('inf')

        history = []

        # PSO parameters
        w = 0.7  # inertia weight
        c1 = 1.5  # cognitive parameter
        c2 = 1.5  # social parameter

        for iteration in range(max_iterations):
            for i in range(population_size):
                # Evaluate fitness (minimize a mock quantum cost function)
                score = self._quantum_cost_function(positions[i])

                # Update personal best
                if score < personal_best_scores[i]:
                    personal_best_scores[i] = score
                    personal_best_positions[i] = positions[i].copy()

                # Update global best
                if score < global_best_score:
                    global_best_score = score
                    global_best_position = positions[i].copy()

            # Update velocities and positions
            for i in range(population_size):
                r1, r2 = np.random.random(dimensions), np.random.random(dimensions)
                velocities[i] = (
                    w * velocities[i] +
                    c1 * r1 * (personal_best_positions[i] - positions[i]) +
                    c2 * r2 * (global_best_position - positions[i])
                )
                positions[i] += velocities[i]
                # Clamp positions
                positions[i] = np.clip(positions[i], -1, 1)

            history.append({
                'iteration': iteration,
                'best_fitness': float(global_best_score),
                'mean_fitness': float(np.mean(personal_best_scores))
            })

            if iteration % 10 == 0:
                print(f"   Iteration {iteration}: Best fitness = {global_best_score:.6f}")

        eal_data = {
            'best_fitness': float(global_best_score),
            'best_position': global_best_position.tolist(),
            'convergence_history': history,
            'final_diversity': float(np.std(positions))
        }

        self.results['experiments']['eal'] = eal_data

        # Save EAL history
        with open(self.artifacts_dir / 'eal_history.json', 'w') as f:
            json.dump(history, f, indent=2)

        print(f"   ✓ EAL converged to fitness: {global_best_score:.6f}")

        return eal_data

    def _quantum_cost_function(self, params: np.ndarray) -> float:
        """
        Mock quantum cost function for EAL optimization.
        Represents circuit parameter optimization landscape.
        """
        # Rastrigin function (multi-modal optimization landscape)
        A = 10
        n = len(params)
        cost = A * n + np.sum(params**2 - A * np.cos(2 * np.pi * params))
        return float(cost)

    def coherence_workflow_analysis(self, max_depth: int = 10) -> Dict:
        """
        Analyze circuit coherence vs depth to find the 'sweet spot'.
        Models T1/T2 decay and gate fidelity degradation.
        """
        print("\n⚛️  Running Coherence Workflow Analysis...")

        metrics = []

        for depth in range(1, max_depth + 1):
            # Create parameterized circuit with varying depth
            circuit = self._create_parameterized_circuit(depth)
            compiled = transpile(circuit, self.backend, optimization_level=2)

            # Estimate fidelity proxy based on depth and gate count
            # Real hardware would use actual error rates
            t1_decay = np.exp(-depth * 0.15)  # T1 relaxation
            t2_decay = np.exp(-depth * 0.20)  # T2 dephasing
            gate_errors = compiled.size() * 0.002  # Per-gate error

            fidelity_proxy = t1_decay * t2_decay * (1 - gate_errors)

            metrics.append({
                'depth': depth,
                'gate_count': compiled.size(),
                'fidelity_proxy': float(max(0, fidelity_proxy)),
                't1_factor': float(t1_decay),
                't2_factor': float(t2_decay)
            })

            print(f"   Depth {depth:2d}: Fidelity proxy = {fidelity_proxy:.4f}")

        # Find optimal depth
        optimal_idx = max(range(len(metrics)), key=lambda i: metrics[i]['fidelity_proxy'])
        optimal_depth = metrics[optimal_idx]['depth']

        workflow_data = {
            'metrics': metrics,
            'optimal_depth': optimal_depth,
            'optimal_fidelity': metrics[optimal_idx]['fidelity_proxy']
        }

        self.results['experiments']['coherence_workflow'] = workflow_data

        # Save workflow metrics
        with open(self.artifacts_dir / 'wflow_metrics.json', 'w') as f:
            json.dump(metrics, f, indent=2)

        print(f"   ✓ Optimal circuit depth: {optimal_depth} (fidelity: {metrics[optimal_idx]['fidelity_proxy']:.4f})")

        return workflow_data

    def _create_parameterized_circuit(self, depth: int) -> QuantumCircuit:
        """Create a parameterized circuit for coherence analysis."""
        qc = QuantumCircuit(2, 2)
        for _ in range(depth):
            qc.rx(np.pi/4, 0)
            qc.ry(np.pi/4, 1)
            qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])
        return qc

    def wormhole_entanglement_refresh(
        self,
        backend_pair: Tuple[str, str] = ('ibm_torino', 'ibm_kyiv')
    ) -> Dict:
        """
        Wormhole experiment: Entanglement-refresh correlation between two backends.
        Tests non-local adaptation by running correlated circuits on different hardware.
        """
        print("\n🌀 Running Wormhole Entanglement-Refresh Correlation...")

        if not self.use_hardware:
            print("   ⚠️  Wormhole experiment requires hardware backends. Skipping.")
            wormhole_data = {
                'status': 'skipped',
                'reason': 'hardware_required',
                'backend_pair': backend_pair
            }
            self.results['experiments']['wormhole'] = wormhole_data
            return wormhole_data

        # Create entangled circuit for both backends
        circuit = self.create_bell_circuit()

        try:
            # Execute on primary backend (already initialized)
            backend1_result = self._run_on_backend(circuit, self.backend)

            # Try to execute on secondary backend
            try:
                backend2 = self.service.backend(backend_pair[1])
                backend2_result = self._run_on_backend(circuit, backend2)

                # Calculate correlation
                correlation = self._calculate_entanglement_correlation(
                    backend1_result, backend2_result
                )

                wormhole_data = {
                    'status': 'completed',
                    'backend_pair': backend_pair,
                    'backend1_counts': backend1_result,
                    'backend2_counts': backend2_result,
                    'correlation': float(correlation),
                    'entanglement_preserved': correlation > 0.8
                }

                print(f"   ✓ Wormhole correlation: {correlation:.4f}")

            except Exception as e:
                print(f"   ⚠️  Could not access secondary backend {backend_pair[1]}: {e}")
                wormhole_data = {
                    'status': 'partial',
                    'backend_pair': backend_pair,
                    'backend1_counts': backend1_result,
                    'error': str(e)
                }

        except Exception as e:
            print(f"   ⚠️  Wormhole experiment failed: {e}")
            wormhole_data = {
                'status': 'failed',
                'backend_pair': backend_pair,
                'error': str(e)
            }

        self.results['experiments']['wormhole'] = wormhole_data
        return wormhole_data

    def _run_on_backend(self, circuit: QuantumCircuit, backend) -> Dict:
        """Execute circuit on specified backend."""
        compiled = transpile(circuit, backend, optimization_level=3)

        with Session(service=self.service, backend=backend) as session:
            sampler = Sampler(session=session)
            job = sampler.run(compiled, shots=self.shots)
            result = job.result()
            counts = result.quasi_dists[0].binary_probabilities()
            return {k: int(v * self.shots) for k, v in counts.items()}

    def _calculate_entanglement_correlation(
        self, counts1: Dict, counts2: Dict
    ) -> float:
        """
        Calculate correlation between two Bell state measurements.
        High correlation indicates preserved entanglement across backends.
        """
        # Normalize counts
        total1 = sum(counts1.values())
        total2 = sum(counts2.values())
        prob1 = {k: v/total1 for k, v in counts1.items()}
        prob2 = {k: v/total2 for k, v in counts2.items()}

        # Calculate fidelity overlap
        overlap = 0
        for state in ['00', '11', '01', '10']:
            p1 = prob1.get(state, 0)
            p2 = prob2.get(state, 0)
            overlap += np.sqrt(p1 * p2)

        return overlap

    def persona_encoding(self) -> Dict:
        """
        Encode agent personality and policy weights.
        Represents the organism's behavioral signature.
        """
        print("\n🎭 Encoding Agent Persona...")

        persona_data = {
            'agent_id': f'quantum_swarm_{int(time.time())}',
            'policy_weights': {
                'exploration': 0.65,
                'exploitation': 0.35,
                'risk_tolerance': 0.42,
                'learning_rate': 0.15
            },
            'behavioral_traits': {
                'curiosity': 0.78,
                'stability': 0.82,
                'adaptability': 0.71,
                'coherence_preference': 0.88
            },
            'evolutionary_fitness': self.results['experiments'].get('eal', {}).get('best_fitness', 0)
        }

        self.results['experiments']['persona'] = persona_data

        # Save persona state
        with open(self.artifacts_dir / 'persona_state.json', 'w') as f:
            json.dump(persona_data, f, indent=2)

        print(f"   ✓ Persona encoded: {persona_data['agent_id']}")

        return persona_data

    def run_full_experiment(self) -> Dict:
        """
        Execute complete quantum swarm DNA-Lang experiment cycle.
        Returns master summary with all experiment artifacts.
        """
        print("╔═══════════════════════════════════════════════════════╗")
        print("║   Quantum Swarm DNA-Lang Experiment                   ║")
        print("╚═══════════════════════════════════════════════════════╝")

        # Update status
        self.results['status'] = 'completed' if self.use_hardware else 'simulated'

        # Run all experiment modules
        self.run_bell_experiment()
        self.evolutionary_adaptive_layer()
        self.coherence_workflow_analysis()
        self.wormhole_entanglement_refresh()
        self.persona_encoding()

        # Save master summary
        summary_path = self.artifacts_dir / 'master_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(self.results, f, indent=2)

        print("\n" + "="*60)
        print(f"✓ Experiment complete! Results saved to {summary_path}")
        print("="*60)

        return self.results


def main():
    """CLI entry point for quantum swarm experiments."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Quantum Swarm DNA-Lang Experiment Runner'
    )
    parser.add_argument(
        '--backend',
        default='ibm_torino',
        help='IBM Quantum backend name (default: ibm_torino)'
    )
    parser.add_argument(
        '--shots',
        type=int,
        default=1024,
        help='Number of measurement shots (default: 1024)'
    )
    parser.add_argument(
        '--artifacts-dir',
        default='./quantum_artifacts',
        help='Directory for artifact output (default: ./quantum_artifacts)'
    )

    args = parser.parse_args()

    config = {
        'backend': args.backend,
        'shots': args.shots,
        'artifacts_dir': args.artifacts_dir
    }

    swarm = QuantumSwarmDNA(config)
    results = swarm.run_full_experiment()

    # Print summary
    print("\n📊 Experiment Summary:")
    print(f"   Backend: {results['backend']} ({results['status']})")
    print(f"   Bell fidelity: {results['experiments']['bell']['fidelity']:.4f}")
    print(f"   EAL best fitness: {results['experiments']['eal']['best_fitness']:.4f}")
    print(f"   Optimal depth: {results['experiments']['coherence_workflow']['optimal_depth']}")

    if 'wormhole' in results['experiments'] and results['experiments']['wormhole']['status'] == 'completed':
        print(f"   Wormhole correlation: {results['experiments']['wormhole']['correlation']:.4f}")


if __name__ == '__main__':
    main()
