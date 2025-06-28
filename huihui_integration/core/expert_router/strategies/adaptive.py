"""
🎯 EXPERT ROUTER - ADAPTIVE ROUTING STRATEGY
==================================================================

This module implements an adaptive routing strategy that combines multiple
routing strategies (e.g., vector-based and performance-based) to make
more informed routing decisions.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum, auto
import random
from datetime import datetime

from data_models.huihui_models import HuiHuiExpertType, RoutingDecision
from .base import BaseRoutingStrategy
from .vector_based import VectorBasedRouting
from .performance_based import PerformanceBasedRouting, PerformanceConfig

logger = logging.getLogger(__name__)

class StrategyType(Enum):
    """Types of routing strategies that can be combined."""
    VECTOR = auto()
    PERFORMANCE = auto()
    RANDOM = auto()
    FALLBACK = auto()

@dataclass
class StrategyWeight:
    """Weight configuration for a routing strategy."""
    strategy_type: StrategyType
    weight: float = 1.0
    config: Optional[Dict[str, Any]] = None
    
    @property
    def strategy_name(self) -> str:
        """Get the strategy name."""
        return self.strategy_type.name.lower()

class AdaptiveRouting(BaseRoutingStrategy):
    """
    An adaptive routing strategy that combines multiple routing strategies
    to make more informed decisions.
    """
    
    def __init__(
        self,
        strategies: Optional[List[StrategyWeight]] = None,
        fallback_expert: HuiHuiExpertType = HuiHuiExpertType.ORCHESTRATOR,
        enable_learning: bool = True,
        exploration_rate: float = 0.1,
        **kwargs
    ):
        """
        Initialize the adaptive routing strategy.
        
        Args:
            strategies: List of strategies and their weights
            fallback_expert: Expert to use when all else fails
            enable_learning: Whether to learn from feedback
            exploration_rate: Probability of exploring a random expert (0.0 to 1.0)
            **kwargs: Additional arguments passed to the base class
        """
        super().__init__(strategy_name="adaptive", **kwargs)
        
        # Default strategies if none provided
        self.strategies = strategies or [
            StrategyWeight(StrategyType.VECTOR, weight=0.7),
            StrategyWeight(StrategyType.PERFORMANCE, weight=0.3)
        ]
        
        self.fallback_expert = fallback_expert
        self.enable_learning = enable_learning
        self.exploration_rate = max(0.0, min(1.0, exploration_rate))
        
        # Initialize strategy instances
        self.strategy_instances: Dict[str, BaseRoutingStrategy] = {}
        self.strategy_weights: Dict[str, float] = {}
        self.strategy_performance: Dict[str, float] = {}
        
        # Track decisions for learning
        self.decision_history: List[Dict[str, Any]] = []
        self.max_history = 1000
        
        # Will be populated in initialize()
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize the strategy and all sub-strategies."""
        if self._initialized:
            return
            
        self.logger.info("Initializing adaptive routing strategy")
        
        # Initialize strategy instances
        for strategy_weight in self.strategies:
            strategy_name = strategy_weight.strategy_name
            self.strategy_weights[strategy_name] = strategy_weight.weight
            self.strategy_performance[strategy_name] = 1.0  # Start with neutral performance
            
            # Initialize the appropriate strategy instance
            if strategy_weight.strategy_type == StrategyType.VECTOR:
                config = strategy_weight.config or {}
                self.strategy_instances[strategy_name] = VectorBasedRouting(
                    **config,
                    logger=self.logger.getChild("vector")
                )
            elif strategy_weight.strategy_type == StrategyType.PERFORMANCE:
                config = strategy_weight.config or {}
                perf_config = config.get("config")
                if perf_config and not isinstance(perf_config, PerformanceConfig):
                    perf_config = PerformanceConfig(**perf_config)
                self.strategy_instances[strategy_name] = PerformanceBasedRouting(
                    config=perf_config,
                    **{k: v for k, v in config.items() if k != "config"},
                    logger=self.logger.getChild("performance")
                )
            elif strategy_weight.strategy_type == StrategyType.RANDOM:
                # Simple random strategy (no initialization needed)
                pass
            elif strategy_weight.strategy_type == StrategyType.FALLBACK:
                # Fallback strategy (always returns fallback expert)
                pass
        
        # Initialize all strategy instances
        for strategy in self.strategy_instances.values():
            if hasattr(strategy, 'initialize'):
                await strategy.initialize()
        
        self._initialized = True
        self.logger.info(f"Initialized adaptive routing with {len(self.strategies)} strategies")
    
    async def select_expert(
        self, 
        prompt: str,
        context: Optional[Dict[str, Any]] = None
    ) -> RoutingDecision:
        """
        Select the best expert using an adaptive combination of strategies.
        
        Args:
            prompt: The input prompt to route
            context: Optional context for the request
            
        Returns:
            A RoutingDecision object with the selected expert and metadata
        """
        if not self._initialized:
            await self.initialize()
        
        # Exploration: Occasionally select a random expert to explore
        if random.random() < self.exploration_rate and self.enable_learning:
            expert_type = random.choice(list(HuiHuiExpertType))
            self.logger.debug(f"Exploring random expert: {expert_type.value}")
            return RoutingDecision(
                expert_type=expert_type,
                confidence=0.1,  # Low confidence for exploration
                strategy_used="exploration",
                metadata={"exploration": True}
            )
        
        # Get decisions from all strategies
        decisions: Dict[str, RoutingDecision] = {}
        
        for strategy_name, strategy in self.strategy_instances.items():
            try:
                decision = await strategy.select_expert(prompt, context)
                decisions[strategy_name] = decision
            except Exception as e:
                self.logger.error(
                    f"Error in {strategy_name} strategy: {str(e)}",
                    exc_info=True
                )
        
        # If no strategies succeeded, use fallback
        if not decisions:
            self.logger.warning("All strategies failed, using fallback expert")
            return RoutingDecision(
                expert_type=self.fallback_expert,
                confidence=0.0,
                strategy_used="fallback",
                metadata={"fallback_reason": "all_strategies_failed"}
            )
        
        # Combine decisions using weighted voting
        expert_votes: Dict[HuiHuiExpertType, float] = {}
        strategy_metadata = {}
        
        for strategy_name, decision in decisions.items():
            weight = self.strategy_weights.get(strategy_name, 1.0)
            performance = self.strategy_performance.get(strategy_name, 1.0)
            
            # Adjust weight by strategy performance
            adjusted_weight = weight * performance
            
            # Add to votes
            if decision.expert_type not in expert_votes:
                expert_votes[decision.expert_type] = 0.0
            
            expert_votes[decision.expert_type] += adjusted_weight * decision.confidence
            
            # Store metadata
            strategy_metadata[strategy_name] = {
                "expert": decision.expert_type.value,
                "confidence": decision.confidence,
                "weight": weight,
                "performance": performance,
                "adjusted_weight": adjusted_weight
            }
        
        # Select expert with highest weighted votes
        if not expert_votes:
            # This should not happen, but just in case
            selected_expert = self.fallback_expert
            confidence = 0.0
        else:
            selected_expert, confidence = max(
                expert_votes.items(),
                key=lambda x: x[1]
            )
            
            # Normalize confidence to [0, 1] range
            total_weight = sum(w * self.strategy_performance.get(name, 1.0) 
                             for name, w in self.strategy_weights.items() 
                             if name in decisions)
            if total_weight > 0:
                confidence = min(1.0, confidence / total_weight)
            else:
                confidence = 0.0
        
        # Prepare metadata
        metadata = {
            "strategies": strategy_metadata,
            "selected_expert": selected_expert.value,
            "confidence": confidence,
            "exploration_rate": self.exploration_rate
        }
        
        # Store decision for learning
        if self.enable_learning:
            self.decision_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "prompt": prompt,
                "selected_expert": selected_expert.value,
                "confidence": confidence,
                "strategies": {
                    name: {
                        "expert": dec.expert_type.value,
                        "confidence": dec.confidence
                    } for name, dec in decisions.items()
                },
                "metadata": metadata
            })
            
            # Trim history if needed
            if len(self.decision_history) > self.max_history:
                self.decision_history = self.decision_history[-self.max_history:]
        
        self.logger.debug(
            f"Selected expert: {selected_expert.value} (confidence: {confidence:.2f})\n"
            f"Strategy votes: {[(e.value, f'{v:.2f}') for e, v in sorted(expert_votes.items(), key=lambda x: x[1], reverse=True)[:3]]}"
        )
        
        return RoutingDecision(
            expert_type=selected_expert,
            confidence=confidence,
            strategy_used=self.strategy_name,
            metadata=metadata
        )
    
    async def update_performance(
        self,
        expert_type: HuiHuiExpertType,
        success: bool,
        response_time: float,
        **kwargs
    ) -> None:
        """
        Update performance metrics based on expert feedback.
        
        Args:
            expert_type: The type of expert
            success: Whether the expert's response was successful
            response_time: How long the expert took to respond (seconds)
            **kwargs: Additional performance metrics
        """
        if not self.enable_learning:
            return
        
        # Update performance for each strategy
        for strategy_name, strategy in self.strategy_instances.items():
            try:
                await strategy.update_performance(
                    expert_type=expert_type,
                    success=success,
                    response_time=response_time,
                    **kwargs
                )
            except Exception as e:
                self.logger.error(
                    f"Error updating performance for {strategy_name}: {str(e)}",
                    exc_info=True
                )
        
        # Update strategy weights based on historical performance
        await self._update_strategy_weights(success, response_time)
    
    async def _update_strategy_weights(
        self, 
        success: bool, 
        response_time: float
    ) -> None:
        """
        Update strategy weights based on recent performance.
        
        Args:
            success: Whether the last expert response was successful
            response_time: Response time of the last expert (seconds)
        """
        if not self.decision_history:
            return
        
        # Get the most recent decision
        last_decision = self.decision_history[-1]
        
        # Calculate reward (higher is better)
        reward = 1.0 if success else -1.0
        # Penalize slow responses
        reward -= min(1.0, response_time / 10.0)  # Normalize to [0,1] range
        
        # Update performance for each strategy that contributed to the decision
        for strategy_name, strategy_info in last_decision.get("strategies", {}).items():
            if strategy_name not in self.strategy_performance:
                continue
                
            # Calculate strategy contribution to the decision
            strategy_confidence = strategy_info.get("confidence", 0.0)
            
            # Update performance with moving average
            learning_rate = 0.1  # How quickly to adapt to new information
            self.strategy_performance[strategy_name] = (
                (1 - learning_rate) * self.strategy_performance[strategy_name] +
                learning_rate * (reward * strategy_confidence)
            )
            
            # Ensure performance stays within reasonable bounds
            self.strategy_performance[strategy_name] = max(
                0.1,  # Minimum performance
                min(2.0, self.strategy_performance[strategy_name])  # Maximum performance
            )
        
        self.logger.debug(
            "Updated strategy performance: " +
            ", ".join(f"{k}: {v:.2f}" for k, v in self.strategy_performance.items())
        )
    
    def get_strategy_state(self) -> Dict[str, Any]:
        """Get the current state of the strategy."""
        state = {
            **super().get_strategy_state(),
            "strategies": {},
            "strategy_weights": self.strategy_weights,
            "strategy_performance": self.strategy_performance,
            "fallback_expert": self.fallback_expert.value,
            "enable_learning": self.enable_learning,
            "exploration_rate": self.exploration_rate,
            "decision_history_size": len(self.decision_history)
        }
        
        # Add state for each strategy
        for name, strategy in self.strategy_instances.items():
            try:
                state["strategies"][name] = strategy.get_strategy_state()
            except Exception as e:
                self.logger.error(
                    f"Error getting state for {name}: {str(e)}",
                    exc_info=True
                )
        
        return state
    
    async def shutdown(self) -> None:
        """Clean up resources used by the strategy."""
        for strategy in self.strategy_instances.values():
            if hasattr(strategy, 'shutdown'):
                try:
                    await strategy.shutdown()
                except Exception as e:
                    self.logger.error(
                        f"Error shutting down strategy {strategy.__class__.__name__}: {str(e)}",
                        exc_info=True
                    )
        
        self._initialized = False
