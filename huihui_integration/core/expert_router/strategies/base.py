"""
🎯 EXPERT ROUTER - BASE ROUTING STRATEGY
==================================================================

This module defines the base class for all routing strategies.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
import logging

from data_models.huihui_models import HuiHuiExpertType, RoutingDecision

logger = logging.getLogger(__name__)

class BaseRoutingStrategy(ABC):
    """
    Abstract base class for all routing strategies.
    
    Subclasses should implement the select_expert method to provide
    expert selection logic.
    """
    
    def __init__(self, strategy_name: str = "base"):
        """
        Initialize the routing strategy.
        
        Args:
            strategy_name: A name for this strategy (used in logging)
        """
        self.strategy_name = strategy_name
        self.logger = logger.getChild(strategy_name)
    
    @abstractmethod
    async def select_expert(
        self, 
        prompt: str,
        context: Optional[Dict[str, Any]] = None
    ) -> RoutingDecision:
        """
        Select the best expert for the given prompt.
        
        Args:
            prompt: The input prompt to route
            context: Optional context for the request
            
        Returns:
            A RoutingDecision object with the selected expert and metadata
        """
        pass
    
    async def update_performance(
        self,
        expert_type: HuiHuiExpertType,
        success: bool,
        response_time: float,
        **kwargs
    ) -> None:
        """
        Update performance metrics for an expert.
        
        Args:
            expert_type: The type of expert
            success: Whether the expert's response was successful
            response_time: How long the expert took to respond (seconds)
            **kwargs: Additional performance metrics
        """
        pass
    
    def get_strategy_state(self) -> Dict[str, Any]:
        """
        Get the current state of the strategy.
        
        Returns:
            A dictionary containing strategy state information
        """
        return {
            "strategy_name": self.strategy_name,
            "strategy_type": self.__class__.__name__
        }
    
    async def initialize(self) -> None:
        """
        Initialize any resources required by the strategy.
        
        This method can be overridden by subclasses to perform
        initialization that requires async operations.
        """
        pass
    
    async def shutdown(self) -> None:
        """
        Clean up any resources used by the strategy.
        
        This method can be overridden by subclasses to perform
        cleanup of resources.
        """
        pass
