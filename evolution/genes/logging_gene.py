"""
Logging verbosity gene for the evolution framework.

This gene handles dynamic logging level adjustment functionality
for organisms in the genomic analysis platform.
"""

import logging
from typing import Any, Dict, Optional

from .base_gene import Gene


class LoggingVerbosityGene(Gene):
    """
    Gene responsible for dynamic logging level management.
    
    This gene allows organisms to dynamically adjust the global logging
    level during runtime based on specified parameters.
    """
    
    # Mapping of string levels to logging constants
    LEVEL_MAPPING = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARN': logging.WARNING,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    def __init__(self, name: str = "logging_verbosity_gene", version: str = "1.0") -> None:
        """
        Initialize the logging verbosity gene.
        
        Args:
            name: The name of the gene (defaults to 'logging_verbosity_gene')
            version: The version of the gene implementation
        """
        super().__init__(name, version)
        self.current_level = 'INFO'
        self.previous_level: Optional[str] = None
        self.level_history = []
        
        # Set up a dedicated logger for this gene
        self.logger = logging.getLogger(f"evolution.genes.{self.name}")
        
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute logging level adjustment functionality.
        
        Args:
            context: Dictionary containing logging configuration
                - level: Target logging level ('DEBUG', 'INFO', 'WARN', 'ERROR')
                - action: 'set_level', 'get_level', 'reset_level'
                - logger_name: Optional specific logger name to modify
                
        Returns:
            Dictionary with logging operation results
        """
        action = context.get('action', 'set_level')
        
        if action == 'set_level':
            return self._set_logging_level(context)
        elif action == 'get_level':
            return self._get_logging_level(context)
        elif action == 'reset_level':
            return self._reset_logging_level(context)
        elif action == 'get_history':
            return self._get_level_history(context)
        else:
            return {'success': False, 'error': f'Unknown action: {action}'}
    
    def _set_logging_level(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set the logging level for the specified or root logger.
        
        Args:
            context: Context containing level and optional logger_name
            
        Returns:
            Result of the logging level change operation
        """
        level = context.get('level', 'INFO').upper()
        logger_name = context.get('logger_name')
        
        # Validate the logging level
        if level not in self.LEVEL_MAPPING:
            return {
                'success': False,
                'error': f'Invalid logging level: {level}. Valid levels: {list(self.LEVEL_MAPPING.keys())}'
            }
        
        try:
            # Store previous level for potential rollback
            if logger_name:
                target_logger = logging.getLogger(logger_name)
                old_level = target_logger.getEffectiveLevel()
            else:
                target_logger = logging.getLogger()  # Root logger
                old_level = target_logger.getEffectiveLevel()
            
            # Convert numeric level back to string for storage
            old_level_name = self._numeric_to_level_name(old_level)
            self.previous_level = old_level_name
            
            # Set the new logging level
            new_level_numeric = self.LEVEL_MAPPING[level]
            target_logger.setLevel(new_level_numeric)
            
            # Update current level tracking
            self.current_level = level
            
            # Record the change in history
            self._record_level_change(old_level_name, level, logger_name)
            
            # Log the change using the gene's logger
            self.logger.info(f"Logging level changed from {old_level_name} to {level}" + 
                           (f" for logger '{logger_name}'" if logger_name else " for root logger"))
            
            return {
                'success': True,
                'previous_level': old_level_name,
                'new_level': level,
                'logger_name': logger_name or 'root',
                'message': f'Logging level successfully changed to {level}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to set logging level: {str(e)}'
            }
    
    def _get_logging_level(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the current logging level for the specified or root logger.
        
        Args:
            context: Context containing optional logger_name
            
        Returns:
            Current logging level information
        """
        logger_name = context.get('logger_name')
        
        try:
            if logger_name:
                target_logger = logging.getLogger(logger_name)
            else:
                target_logger = logging.getLogger()  # Root logger
            
            current_numeric_level = target_logger.getEffectiveLevel()
            current_level_name = self._numeric_to_level_name(current_numeric_level)
            
            return {
                'success': True,
                'current_level': current_level_name,
                'numeric_level': current_numeric_level,
                'logger_name': logger_name or 'root',
                'gene_tracked_level': self.current_level
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to get logging level: {str(e)}'
            }
    
    def _reset_logging_level(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reset the logging level to the previous level.
        
        Args:
            context: Context for reset operation
            
        Returns:
            Result of the reset operation
        """
        if not self.previous_level:
            return {
                'success': False,
                'error': 'No previous logging level available to reset to'
            }
        
        # Use the previous level to reset
        reset_context = {
            'level': self.previous_level,
            'logger_name': context.get('logger_name')
        }
        
        result = self._set_logging_level(reset_context)
        if result['success']:
            result['message'] = f'Logging level reset to previous level: {self.previous_level}'
        
        return result
    
    def _get_level_history(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the history of logging level changes.
        
        Args:
            context: Context for history request
            
        Returns:
            History of logging level changes
        """
        return {
            'success': True,
            'level_history': self.level_history,
            'current_level': self.current_level,
            'previous_level': self.previous_level
        }
    
    def _numeric_to_level_name(self, numeric_level: int) -> str:
        """
        Convert numeric logging level to string name.
        
        Args:
            numeric_level: Numeric logging level
            
        Returns:
            String name of the logging level
        """
        level_reverse_mapping = {v: k for k, v in self.LEVEL_MAPPING.items()}
        return level_reverse_mapping.get(numeric_level, 'UNKNOWN')
    
    def _record_level_change(self, old_level: str, new_level: str, logger_name: Optional[str]) -> None:
        """
        Record a logging level change in the history.
        
        Args:
            old_level: Previous logging level
            new_level: New logging level
            logger_name: Name of the logger that was modified
        """
        import time
        
        change_record = {
            'timestamp': time.time(),
            'old_level': old_level,
            'new_level': new_level,
            'logger_name': logger_name or 'root',
            'gene_name': self.name
        }
        
        self.level_history.append(change_record)
        
        # Keep only the last 50 changes to prevent memory growth
        if len(self.level_history) > 50:
            self.level_history = self.level_history[-50:]