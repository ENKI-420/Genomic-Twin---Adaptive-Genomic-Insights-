"""
Base gene class for the evolution framework.

This module defines the base Gene class that all specific gene implementations
should inherit from.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Gene(ABC):
    """
    Base class for all genes in the evolution framework.
    
    Genes are functional units that can modify organism behavior.
    Each gene must implement an execute method that performs its function.
    """
    
    def __init__(self, name: str, version: str = "1.0") -> None:
        """
        Initialize a gene.
        
        Args:
            name: The name of the gene
            version: The version of the gene implementation
        """
        self.name = name
        self.version = version
        self.active = True
        
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        """
        Execute the gene's functionality.
        
        Args:
            context: The execution context containing relevant data
            
        Returns:
            Any result from the gene execution
        """
        pass
        
    def activate(self) -> None:
        """Activate this gene."""
        self.active = True
        
    def deactivate(self) -> None:
        """Deactivate this gene."""
        self.active = False
        
    def is_active(self) -> bool:
        """
        Check if the gene is active.
        
        Returns:
            True if the gene is active, False otherwise
        """
        return self.active
        
    def __repr__(self) -> str:
        """String representation of the gene."""
        status = "active" if self.active else "inactive"
        return f"{self.__class__.__name__}(name='{self.name}', version='{self.version}', status='{status}')"