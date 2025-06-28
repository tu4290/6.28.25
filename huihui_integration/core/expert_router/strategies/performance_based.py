"""
🎯 EXPERT ROUTER - PERFORMANCE-BASED ROUTING STRATEGY
==================================================================

This module implements a performance-based routing strategy that routes queries
to experts based on their historical performance metrics.
"""

import logging
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

from data_models.huihui_models import HuiHuiExpertType, RoutingDecision, PerformanceMetrics, ExpertPerformance
from .base import BaseRoutingStrategy

logger = logging.getLogger(__name__)

@dataclass
class PerformanceConfig:
    """Configuration for performance-based routing."""
    # Weight for success rate (0.0 to 1.0)
    success_rate_weight: float = 0.6
    
    # Weight for response time (0.0 to 1.0)
    response_time_weight: float = 0.3
    
    # Weight for recent usage (0.0 to 1.0)
    recent_usage_weight: float = 0.1
    
    # Time window for recent usage (seconds)
    recent_usage_window: int = 3600  # 1 hour
    
    # Minimum number of queries required to consider an expert's metrics
    min_queries_for_confidence: int = 5
    
    # Default success rate for experts with insufficient data
    default_success_rate: float = 0.8
    
    # Default response time for experts with insufficient data (seconds)
    default_response_time: float = 2.0
    
    # Maximum allowed response time before penalizing (seconds)
    max_allowed_response_time: float = 10.0
    
    # Decay factor for older performance data (0.0 to 1.0)
    decay_factor: float = 0.95

class PerformanceBasedRouting(BaseRoutingStrategy):
    """
    A routing strategy that selects experts based on their historical performance
    metrics such as success rate, response time, and recent usage.
    """
    
    def __init__(self, config: Optional[PerformanceConfig] = None):
        """
        Initialize the performance-based routing strategy.
        
        Args:
            config: Configuration for the performance-based router
            **kwargs: Additional arguments passed to the base class
        """
        super().__init__(strategy_name="performance_based")
        self.config = config or PerformanceConfig()
        self.performance_data: Dict[HuiHuiExpertType, ExpertPerformance] = {}
        self._last_cleanup = datetime.utcnow()
        self._cleanup_interval = 3600  # 1 hour
    
    async def initialize(self) -> None:
        """Initialize the strategy."""
        # Initialize performance data for all expert types
        for expert_type in HuiHuiExpertType:
            self.performance_data[expert_type] = ExpertPerformance()
        
        self.logger.info("Initialized performance-based routing strategy")
    
    def _cleanup_old_data(self) -> None:
        """Clean up old performance data to keep memory usage in check."""
        now = datetime.utcnow()
        if (now - self._last_cleanup).total_seconds() < self._cleanup_interval:
            return
            
        self.logger.debug("Cleaning up old performance data")
        cutoff = now - timedelta(days=7)  # Keep 1 week of data
        
        for expert_type, perf in self.performance_data.items():
            # This is a no-op if the implementation doesn't store timestamps
            pass
            
        self._last_cleanup = now
    
    def _calculate_expert_score(
        self,
        expert_type: HuiHuiExpertType,
        recent_usage: Dict[HuiHuiExpertType, int]
    ) -> float:
        """
        Calculate a score for an expert based on performance metrics.
        
        Args:
            expert_type: The expert type to score
            recent_usage: Dictionary of recent usage counts by expert type
            
        Returns:
            A score between 0.0 and 1.0, where higher is better
        """
        perf = self.performance_data.get(expert_type)
        if perf is None:
            return 0.0
            
        metrics = perf.metrics.get(expert_type, PerformanceMetrics())
        
        # Calculate success rate component
        if metrics.total_queries >= self.config.min_queries_for_confidence:
            success_rate = metrics.success_rate
        else:
            # Use default for experts with insufficient data
            success_rate = self.config.default_success_rate
        
        # Calculate response time component (lower is better, so we invert it)
        if metrics.successful_queries > 0 and metrics.average_response_time > 0:
            # Normalize response time to 0-1 range (inverted).
            # A lower response time results in a higher score.
            normalized_time = min(metrics.average_response_time, self.config.max_allowed_response_time)
            response_time_score = 1.0 - (normalized_time / self.config.max_allowed_response_time)
        else:
            # Use default response time for scoring
            normalized_time = min(self.config.default_response_time, self.config.max_allowed_response_time)
            response_time_score = 1.0 - (normalized_time / self.config.max_allowed_response_time)
        
        # Calculate recent usage component (lower is better, so we invert it)
        total_recent_queries = sum(recent_usage.values()) or 1
        usage_ratio = recent_usage.get(expert_type, 0) / total_recent_queries
        usage_score = 1.0 - min(1.0, usage_ratio * 2)  # Penalize heavily used experts
        
        # Calculate weighted score
        score = (
            self.config.success_rate_weight * success_rate +
            self.config.response_time_weight * response_time_score +
            self.config.recent_usage_weight * usage_score
        )
        
        # Apply decay based on last usage (optional)
        if metrics.last_used:
            days_since_use = (datetime.utcnow() - metrics.last_used).days
            decay = self.config.decay_factor ** days_since_use
            score *= decay
        
        return max(0.0, min(1.0, score))
    
    async def select_expert(
        self, 
        prompt: str,
        context: Optional[Dict[str, Any]] = None
    ) -> RoutingDecision:
        """
        Select the best expert based on performance metrics.
        
        Args:
            prompt: The input prompt to route
            context: Optional context for the request
            
        Returns:
            A RoutingDecision object with the selected expert and metadata
        """
        self._cleanup_old_data()
        
        # Get recent usage counts
        recent_usage = {}
        for expert_type in self.performance_data:
            recent_usage[expert_type] = self.performance_data[expert_type].get_recent_usage(
                window_seconds=self.config.recent_usage_window
            ).get(expert_type, 0)
        
        # Calculate scores for all experts
        expert_scores = {
            expert_type: self._calculate_expert_score(expert_type, recent_usage)
            for expert_type in self.performance_data
        }
        
        # Select the expert with the highest score
        if not expert_scores:
            # Fallback to orchestrator if no experts available
            return RoutingDecision(
                expert_type=HuiHuiExpertType.ORCHESTRATOR,
                confidence=0.0,
                strategy_used=self.strategy_name,
                metadata={"fallback_reason": "no_experts_available"}
            )
        
        # Get the best expert and its score
        best_expert = max(expert_scores.items(), key=lambda x: x[1])
        
        # Prepare metadata
        metadata = {
            "scores": {
                expert.value: float(score)
                for expert, score in sorted(
                    expert_scores.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
            },
            "selected_expert": best_expert[0].value,
            "selected_score": float(best_expert[1])
        }
        
        self.logger.debug(
            f"Selected expert: {best_expert[0].value} (score: {best_expert[1]:.2f})\n"
            f"Top candidates: {[(e.value, f'{s:.2f}') for e, s in sorted(expert_scores.items(), key=lambda x: x[1], reverse=True)[:3]]}"
        )
        
        return RoutingDecision(
            expert_type=best_expert[0],
            confidence=best_expert[1],
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
        Update performance metrics for an expert.
        
        Args:
            expert_type: The type of expert
            success: Whether the expert's response was successful
            response_time: How long the expert took to respond (seconds)
            **kwargs: Additional performance metrics
        """
        if expert_type not in self.performance_data:
            self.performance_data[expert_type] = ExpertPerformance()
        
        self.performance_data[expert_type].update_metrics(
            expert_type=expert_type,
            success=success,
            response_time=response_time
        )
        
        self.logger.debug(
            f"Updated performance for {expert_type.value}: "
            f"success={success}, response_time={response_time:.2f}s"
        )
    
    def get_strategy_state(self) -> Dict[str, Any]:
        """Get the current state of the strategy."""
        stats = {
            **super().get_strategy_state(),
            "num_experts": len(self.performance_data),
            "config": {
                "success_rate_weight": self.config.success_rate_weight,
                "response_time_weight": self.config.response_time_weight,
                "recent_usage_weight": self.config.recent_usage_weight,
                "recent_usage_window": self.config.recent_usage_window,
                "min_queries_for_confidence": self.config.min_queries_for_confidence,
                "default_success_rate": self.config.default_success_rate,
                "default_response_time": self.config.default_response_time,
                "max_allowed_response_time": self.config.max_allowed_response_time,
                "decay_factor": self.config.decay_factor
            }
        }
        
        # Add performance summary
        expert_stats = {}
        for expert_type, perf in self.performance_data.items():
            metrics = perf.metrics.get(expert_type)
            if metrics:
                expert_stats[expert_type.value] = {
                    "total_queries": metrics.total_queries,
                    "success_rate": metrics.success_rate,
                    "avg_response_time": metrics.average_response_time,
                    "last_used": metrics.last_used.isoformat() if metrics.last_used else None
                }
        
        stats["expert_stats"] = expert_stats
        return stats
