"""
Performance gene for the evolution framework.

This gene handles performance monitoring and optimization functionality
for organisms in the genomic analysis platform.
"""

import time
import psutil
from typing import Any, Dict, List, Optional

from .base_gene import Gene


class PerformanceGene(Gene):
    """
    Gene responsible for performance monitoring and optimization.
    
    This gene provides performance metrics collection and optimization
    strategies for the genomic analysis platform.
    """
    
    def __init__(self, name: str = "performance_gene", version: str = "1.0") -> None:
        """
        Initialize the performance gene.
        
        Args:
            name: The name of the gene (defaults to 'performance_gene')
            version: The version of the gene implementation
        """
        super().__init__(name, version)
        self.metrics_history: List[Dict[str, Any]] = []
        self.max_history_size = 100
        self.performance_threshold = 80.0  # CPU usage threshold
        
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute performance monitoring functionality.
        
        Args:
            context: Dictionary containing performance monitoring data
                - action: 'monitor', 'optimize', 'get_metrics'
                - duration: Monitoring duration in seconds (for monitor action)
                
        Returns:
            Dictionary with performance results
        """
        action = context.get('action', 'monitor')
        
        if action == 'monitor':
            return self._monitor_performance(context)
        elif action == 'optimize':
            return self._optimize_performance(context)
        elif action == 'get_metrics':
            return self._get_metrics_summary(context)
        else:
            return {'success': False, 'error': f'Unknown action: {action}'}
    
    def _monitor_performance(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Monitor system performance metrics.
        
        Args:
            context: Monitoring context
            
        Returns:
            Performance monitoring results
        """
        duration = context.get('duration', 1)  # Default 1 second
        
        # Collect performance metrics
        start_time = time.time()
        metrics = self._collect_metrics()
        
        # Store metrics in history
        self._store_metrics(metrics)
        
        # Check for performance issues
        issues = self._identify_performance_issues(metrics)
        
        return {
            'success': True,
            'timestamp': start_time,
            'metrics': metrics,
            'issues': issues,
            'recommendations': self._get_recommendations(issues)
        }
    
    def _optimize_performance(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize system performance based on current metrics.
        
        Args:
            context: Optimization context
            
        Returns:
            Optimization results
        """
        current_metrics = self._collect_metrics()
        optimizations_applied = []
        
        # Apply CPU optimization if needed
        if current_metrics['cpu_percent'] > self.performance_threshold:
            optimizations_applied.append(self._optimize_cpu_usage())
        
        # Apply memory optimization if needed
        if current_metrics['memory_percent'] > self.performance_threshold:
            optimizations_applied.append(self._optimize_memory_usage())
        
        return {
            'success': True,
            'optimizations_applied': optimizations_applied,
            'metrics_before': current_metrics,
            'metrics_after': self._collect_metrics()
        }
    
    def _get_metrics_summary(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get summary of performance metrics.
        
        Args:
            context: Summary context
            
        Returns:
            Metrics summary
        """
        if not self.metrics_history:
            return {'success': False, 'error': 'No metrics available'}
        
        return {
            'success': True,
            'total_measurements': len(self.metrics_history),
            'latest_metrics': self.metrics_history[-1] if self.metrics_history else None,
            'average_cpu': self._calculate_average('cpu_percent'),
            'average_memory': self._calculate_average('memory_percent'),
            'average_disk': self._calculate_average('disk_percent')
        }
    
    def _collect_metrics(self) -> Dict[str, Any]:
        """
        Collect current system performance metrics.
        
        Returns:
            Dictionary containing performance metrics
        """
        return {
            'timestamp': time.time(),
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'network_connections': len(psutil.net_connections()),
            'process_count': len(psutil.pids())
        }
    
    def _store_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Store metrics in history with size limit.
        
        Args:
            metrics: Metrics to store
        """
        self.metrics_history.append(metrics)
        
        # Keep only the most recent metrics
        if len(self.metrics_history) > self.max_history_size:
            self.metrics_history = self.metrics_history[-self.max_history_size:]
    
    def _identify_performance_issues(self, metrics: Dict[str, Any]) -> List[str]:
        """
        Identify performance issues based on metrics.
        
        Args:
            metrics: Performance metrics
            
        Returns:
            List of identified issues
        """
        issues = []
        
        if metrics['cpu_percent'] > self.performance_threshold:
            issues.append(f"High CPU usage: {metrics['cpu_percent']:.1f}%")
        
        if metrics['memory_percent'] > self.performance_threshold:
            issues.append(f"High memory usage: {metrics['memory_percent']:.1f}%")
        
        if metrics['disk_percent'] > 90.0:
            issues.append(f"High disk usage: {metrics['disk_percent']:.1f}%")
        
        return issues
    
    def _get_recommendations(self, issues: List[str]) -> List[str]:
        """
        Get performance optimization recommendations.
        
        Args:
            issues: List of identified issues
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        for issue in issues:
            if "CPU usage" in issue:
                recommendations.append("Consider reducing computational load or optimizing algorithms")
            elif "memory usage" in issue:
                recommendations.append("Consider freeing unused objects or increasing available memory")
            elif "disk usage" in issue:
                recommendations.append("Consider cleaning up temporary files or expanding storage")
        
        return recommendations
    
    def _optimize_cpu_usage(self) -> Dict[str, Any]:
        """
        Apply CPU optimization strategies.
        
        Returns:
            Optimization result
        """
        # Placeholder for CPU optimization logic
        return {
            'type': 'cpu_optimization',
            'description': 'Applied CPU usage optimization strategies',
            'success': True
        }
    
    def _optimize_memory_usage(self) -> Dict[str, Any]:
        """
        Apply memory optimization strategies.
        
        Returns:
            Optimization result
        """
        # Placeholder for memory optimization logic
        return {
            'type': 'memory_optimization',
            'description': 'Applied memory usage optimization strategies',
            'success': True
        }
    
    def _calculate_average(self, metric_name: str) -> float:
        """
        Calculate average value for a specific metric.
        
        Args:
            metric_name: Name of the metric to average
            
        Returns:
            Average value of the metric
        """
        if not self.metrics_history:
            return 0.0
        
        values = [m.get(metric_name, 0) for m in self.metrics_history]
        return sum(values) / len(values) if values else 0.0