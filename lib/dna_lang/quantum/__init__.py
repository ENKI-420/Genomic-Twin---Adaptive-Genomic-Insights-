"""
DNA-Lang Quantum Module

W1-Optimized Quantum-Classical Co-Design Framework
for Agile Defense Systems
"""

from .qwc_pass_manager import build_qwc_pass_manager, transpile_with_qwc
from .barren_plateau_diagnostics import diagnose_barren_plateau
from .fidelity_benchmarking import (
    calculate_qwc_target_cost,
    calculate_hardware_cost,
    calculate_fidelity_deviation,
    benchmark_circuit_fidelity,
)
from .optimizer_feedback_api import OptimizerFeedbackAPI

__all__ = [
    "build_qwc_pass_manager",
    "transpile_with_qwc",
    "diagnose_barren_plateau",
    "calculate_qwc_target_cost",
    "calculate_hardware_cost",
    "calculate_fidelity_deviation",
    "benchmark_circuit_fidelity",
    "OptimizerFeedbackAPI",
]
