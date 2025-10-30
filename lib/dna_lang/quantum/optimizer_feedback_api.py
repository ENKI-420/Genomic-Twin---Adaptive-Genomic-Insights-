"""
Optimizer Feedback API

This module implements the API for passing the W1 Fidelity Deviation
metric back to the classical optimizer, thereby closing the self-optimizing
loop and enabling multi-objective fidelity-aware optimization.

The API allows the classical optimizer to incorporate real hardware
fidelity as a constraint or objective, ensuring optimization is driven
by practical, achievable hardware fidelity rather than abstract cost alone.
"""

import numpy as np
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum


class OptimizationMode(Enum):
    """Optimization mode for incorporating fidelity feedback."""
    CONSTRAINT = "constraint"  # Fidelity as hard constraint
    PENALTY = "penalty"  # Fidelity as penalty term
    MULTI_OBJECTIVE = "multi_objective"  # Separate objective


@dataclass
class FidelityConstraint:
    """Configuration for fidelity-aware optimization."""
    
    mode: OptimizationMode = OptimizationMode.PENALTY
    
    # For CONSTRAINT mode
    max_fidelity_deviation: float = 0.1  # Maximum allowed deviation
    
    # For PENALTY mode
    penalty_weight: float = 1.0  # Weight for penalty term
    penalty_type: str = "quadratic"  # "linear", "quadratic", "exponential"
    
    # For MULTI_OBJECTIVE mode
    fidelity_weight: float = 0.5  # Weight for fidelity objective (0-1)
    cost_weight: float = 0.5  # Weight for cost objective (0-1)
    
    # General settings
    adaptive_weight: bool = False  # Adapt weights during optimization
    min_samples_for_feedback: int = 5  # Minimum samples before using feedback


@dataclass
class OptimizationState:
    """State tracking for fidelity-aware optimization."""
    
    iteration: int = 0
    cost_history: List[float] = field(default_factory=list)
    fidelity_history: List[float] = field(default_factory=list)
    parameter_history: List[np.ndarray] = field(default_factory=list)
    
    best_cost: Optional[float] = None
    best_fidelity: Optional[float] = None
    best_parameters: Optional[np.ndarray] = None
    
    constraint_violations: int = 0
    converged: bool = False


class OptimizerFeedbackAPI:
    """
    API for integrating W1 fidelity deviation into classical optimization.
    
    This class provides methods to incorporate real-time hardware fidelity
    feedback into variational quantum algorithms, enabling the optimizer
    to balance abstract cost minimization with practical hardware fidelity.
    
    Example:
        >>> from scipy.optimize import minimize
        >>> 
        >>> # Create feedback API
        >>> feedback_api = OptimizerFeedbackAPI(
        ...     constraint=FidelityConstraint(
        ...         mode=OptimizationMode.PENALTY,
        ...         penalty_weight=0.5
        ...     )
        ... )
        >>> 
        >>> # Define cost function with fidelity feedback
        >>> def cost_function(params):
        ...     # Execute circuit and measure
        ...     qwc_target = calculate_qwc_target_cost(circuit, obs, params)
        ...     hardware_cost = calculate_hardware_cost(circuit, obs, backend, params)
        ...     fidelity_dev = abs(hardware_cost - qwc_target)
        ...     
        ...     # Incorporate fidelity feedback
        ...     return feedback_api.compute_objective(
        ...         cost=hardware_cost,
        ...         fidelity_deviation=fidelity_dev,
        ...         parameters=params
        ...     )
        >>> 
        >>> # Run optimization
        >>> result = minimize(cost_function, initial_params, method='COBYLA')
    """
    
    def __init__(
        self,
        constraint: Optional[FidelityConstraint] = None,
    ):
        """
        Initialize the Optimizer Feedback API.
        
        Args:
            constraint: Fidelity constraint configuration
        """
        self.constraint = constraint or FidelityConstraint()
        self.state = OptimizationState()
    
    def compute_objective(
        self,
        cost: float,
        fidelity_deviation: float,
        parameters: Optional[np.ndarray] = None,
    ) -> float:
        """
        Compute the objective value incorporating fidelity feedback.
        
        Args:
            cost: The base cost from circuit execution
            fidelity_deviation: W1 fidelity deviation metric
            parameters: Current parameter values
        
        Returns:
            Modified objective value for optimizer
        """
        # Update state
        self.state.iteration += 1
        self.state.cost_history.append(cost)
        self.state.fidelity_history.append(fidelity_deviation)
        if parameters is not None:
            self.state.parameter_history.append(parameters.copy())
        
        # Check if we have enough samples
        if self.state.iteration < self.constraint.min_samples_for_feedback:
            return cost  # Return raw cost initially
        
        # Compute objective based on mode
        if self.constraint.mode == OptimizationMode.CONSTRAINT:
            return self._constraint_mode(cost, fidelity_deviation)
        elif self.constraint.mode == OptimizationMode.PENALTY:
            return self._penalty_mode(cost, fidelity_deviation)
        elif self.constraint.mode == OptimizationMode.MULTI_OBJECTIVE:
            return self._multi_objective_mode(cost, fidelity_deviation)
        else:
            return cost
    
    def _constraint_mode(self, cost: float, fidelity_deviation: float) -> float:
        """Implement hard constraint on fidelity deviation."""
        if fidelity_deviation > self.constraint.max_fidelity_deviation:
            self.state.constraint_violations += 1
            # Return large penalty for constraint violation
            violation_penalty = 1e6 * (
                fidelity_deviation - self.constraint.max_fidelity_deviation
            )
            return cost + violation_penalty
        return cost
    
    def _penalty_mode(self, cost: float, fidelity_deviation: float) -> float:
        """Add fidelity deviation as penalty term."""
        weight = self.constraint.penalty_weight
        
        # Adapt weight if enabled
        if self.constraint.adaptive_weight and len(self.state.fidelity_history) > 10:
            # Increase weight if fidelity is degrading
            recent_fidelity = np.mean(self.state.fidelity_history[-10:])
            older_fidelity = np.mean(self.state.fidelity_history[-20:-10]) if len(self.state.fidelity_history) >= 20 else recent_fidelity
            
            if recent_fidelity > older_fidelity * 1.2:
                weight *= 1.5  # Increase penalty if fidelity degrading
        
        # Compute penalty based on type
        if self.constraint.penalty_type == "linear":
            penalty = weight * fidelity_deviation
        elif self.constraint.penalty_type == "quadratic":
            penalty = weight * (fidelity_deviation ** 2)
        elif self.constraint.penalty_type == "exponential":
            penalty = weight * (np.exp(fidelity_deviation) - 1)
        else:
            penalty = weight * fidelity_deviation
        
        return cost + penalty
    
    def _multi_objective_mode(self, cost: float, fidelity_deviation: float) -> float:
        """Combine cost and fidelity as weighted objectives."""
        # Normalize objectives (using history for scaling)
        if len(self.state.cost_history) > 1:
            cost_std = np.std(self.state.cost_history)
            fidelity_std = np.std(self.state.fidelity_history)
            
            norm_cost = cost / (cost_std + 1e-10)
            norm_fidelity = fidelity_deviation / (fidelity_std + 1e-10)
        else:
            norm_cost = cost
            norm_fidelity = fidelity_deviation
        
        # Compute weighted sum
        objective = (
            self.constraint.cost_weight * norm_cost +
            self.constraint.fidelity_weight * norm_fidelity
        )
        
        return objective
    
    def update_best(self, cost: float, fidelity_deviation: float, parameters: np.ndarray):
        """
        Update best solution tracking.
        
        Args:
            cost: Current cost value
            fidelity_deviation: Current fidelity deviation
            parameters: Current parameters
        """
        # Update best based on multi-objective criteria
        if self.state.best_cost is None:
            self.state.best_cost = cost
            self.state.best_fidelity = fidelity_deviation
            self.state.best_parameters = parameters.copy()
        else:
            # Better if: lower cost AND lower/similar fidelity
            # OR: similar cost AND much better fidelity
            cost_improvement = (cost < self.state.best_cost * 0.95)
            fidelity_improvement = (fidelity_deviation < self.state.best_fidelity * 0.95)
            
            if cost_improvement or (
                abs(cost - self.state.best_cost) < 0.01 * abs(self.state.best_cost) and
                fidelity_improvement
            ):
                self.state.best_cost = cost
                self.state.best_fidelity = fidelity_deviation
                self.state.best_parameters = parameters.copy()
    
    def check_convergence(
        self,
        tolerance: float = 1e-6,
        window_size: int = 10,
    ) -> bool:
        """
        Check if optimization has converged.
        
        Args:
            tolerance: Convergence tolerance
            window_size: Window size for checking convergence
        
        Returns:
            True if converged
        """
        if len(self.state.cost_history) < window_size:
            return False
        
        recent_costs = self.state.cost_history[-window_size:]
        cost_variation = np.std(recent_costs) / (abs(np.mean(recent_costs)) + 1e-10)
        
        if cost_variation < tolerance:
            self.state.converged = True
            return True
        
        return False
    
    def get_optimization_summary(self) -> Dict[str, Any]:
        """
        Get summary of optimization progress.
        
        Returns:
            Dictionary with optimization statistics
        """
        return {
            'iterations': self.state.iteration,
            'best_cost': self.state.best_cost,
            'best_fidelity': self.state.best_fidelity,
            'final_cost': self.state.cost_history[-1] if self.state.cost_history else None,
            'final_fidelity': self.state.fidelity_history[-1] if self.state.fidelity_history else None,
            'constraint_violations': self.state.constraint_violations,
            'converged': self.state.converged,
            'cost_improvement': (
                (self.state.cost_history[0] - self.state.best_cost) / abs(self.state.cost_history[0])
                if self.state.cost_history and self.state.best_cost else None
            ),
            'avg_fidelity': np.mean(self.state.fidelity_history) if self.state.fidelity_history else None,
        }
    
    def reset(self):
        """Reset optimization state."""
        self.state = OptimizationState()


def create_fidelity_aware_cost_function(
    base_cost_function: Callable,
    fidelity_function: Callable,
    feedback_api: OptimizerFeedbackAPI,
) -> Callable:
    """
    Create a fidelity-aware cost function wrapper.
    
    This convenience function wraps a base cost function to automatically
    incorporate fidelity feedback through the API.
    
    Args:
        base_cost_function: Original cost function f(params) -> cost
        fidelity_function: Function to compute fidelity f(params) -> fidelity_dev
        feedback_api: Configured feedback API instance
    
    Returns:
        Wrapped cost function with fidelity awareness
    
    Example:
        >>> def my_cost(params):
        ...     return execute_and_measure(params)
        >>> 
        >>> def my_fidelity(params):
        ...     target = calculate_qwc_target_cost(...)
        ...     hardware = calculate_hardware_cost(...)
        ...     return abs(hardware - target)
        >>> 
        >>> api = OptimizerFeedbackAPI()
        >>> wrapped_cost = create_fidelity_aware_cost_function(
        ...     my_cost, my_fidelity, api
        ... )
        >>> result = minimize(wrapped_cost, initial_params)
    """
    def wrapped_cost_function(parameters: np.ndarray) -> float:
        # Compute base cost
        cost = base_cost_function(parameters)
        
        # Compute fidelity deviation
        fidelity_dev = fidelity_function(parameters)
        
        # Incorporate fidelity feedback
        objective = feedback_api.compute_objective(cost, fidelity_dev, parameters)
        
        # Update best solution
        feedback_api.update_best(cost, fidelity_dev, parameters)
        
        return objective
    
    return wrapped_cost_function
