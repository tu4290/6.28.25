"""
🎯 EXPERT ROUTER - VECTOR-BASED ROUTING STRATEGY
==================================================================

This module implements a vector-based routing strategy that uses semantic
similarity to route queries to the most appropriate expert.
"""

import logging
import asyncio
import aiohttp
import numpy as np
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from data_models.huihui_models import HuiHuiExpertType, RoutingDecision
from ..cache import UltraFastEmbeddingCache
from .base import BaseRoutingStrategy

logger = logging.getLogger(__name__)

@dataclass
class ExpertProfile:
    """Represents an expert's profile with associated keywords and descriptions."""
    expert_type: HuiHuiExpertType
    keywords: List[str]
    description: str
    examples: Optional[List[str]] = field(default_factory=list)
    
    def to_embedding_text(self) -> str:
        """Convert the expert profile to a text string for embedding."""
        examples_text = "\n".join(f"- {ex}" for ex in (self.examples or []))
        return (
            f"Expert Type: {self.expert_type.value}\n"
            f"Description: {self.description}\n"
            f"Keywords: {', '.join(self.keywords)}\n"
            f"Example Queries:\n{examples_text}"
        )

class VectorBasedRouting(BaseRoutingStrategy):
    """
    A routing strategy that uses vector embeddings to determine the most
    appropriate expert for a given query based on semantic similarity.
    """
    
    # Default expert profiles (can be overridden)
    DEFAULT_EXPERTS = [
        ExpertProfile(
            expert_type=HuiHuiExpertType.MARKET_REGIME,
            keywords=["market regime", "regime", "market state", "regime change", "market environment"],
            description=(
                "Specializes in identifying and analyzing different market regimes "
                "such as trending, ranging, volatile, or stable markets."
            ),
            examples=[
                "What's the current market regime?",
                "Has the market regime changed recently?",
                "Is this a high volatility environment?"
            ]
        ),
        ExpertProfile(
            expert_type=HuiHuiExpertType.OPTIONS_FLOW,
            keywords=["options flow", "unusual options activity", "options order flow", "block trades"],
            description=(
                "Analyzes options market data to identify unusual activity, "
                "large trades, and potential smart money flows."
            ),
            examples=[
                "Show me unusual options activity in tech stocks",
                "What are the largest options trades today?",
                "Is there any unusual put buying in SPY?"
            ]
        ),
        ExpertProfile(
            expert_type=HuiHuiExpertType.SENTIMENT,
            keywords=["sentiment", "market sentiment", "investor sentiment", "fear and greed"],
            description=(
                "Analyzes market sentiment using news, social media, and other "
                "alternative data sources to gauge market psychology."
            ),
            examples=[
                "What's the current market sentiment?",
                "Is there excessive bullishness in tech stocks?",
                "Show me the fear and greed index"
            ]
        ),
        ExpertProfile(
            expert_type=HuiHuiExpertType.ORCHESTRATOR,
            keywords=["orchestrator", "general", "multi-expert", "complex query"],
            description=(
                "Coordinates complex queries that require input from multiple "
                "specialized experts and synthesizes the results."
            ),
            examples=[
                "Analyze the current market environment",
                "Provide a comprehensive market analysis",
                "What's happening in the markets today?"
            ]
        ),
        ExpertProfile(
            expert_type=HuiHuiExpertType.VOLATILITY,
            keywords=["volatility", "VIX", "implied volatility", "vol surface", "volatility analysis"],
            description=(
                "Specializes in volatility analysis, implied volatility surfaces, "
                "and volatility-based trading strategies."
            ),
            examples=[
                "What's the current VIX level telling us?",
                "Analyze the implied volatility surface for SPY",
                "Is volatility elevated in tech stocks?"
            ]
        ),
        ExpertProfile(
            expert_type=HuiHuiExpertType.LIQUIDITY,
            keywords=["liquidity", "bid-ask spread", "volume", "market depth", "liquidity analysis"],
            description=(
                "Analyzes market liquidity conditions, bid-ask spreads, "
                "and volume patterns for optimal execution."
            ),
            examples=[
                "What's the liquidity like in SPY options?",
                "Analyze the bid-ask spreads for AAPL",
                "Is there sufficient volume for this trade?"
            ]
        ),
        ExpertProfile(
            expert_type=HuiHuiExpertType.RISK,
            keywords=["risk", "risk management", "position sizing", "portfolio risk", "VaR"],
            description=(
                "Focuses on risk assessment, position sizing, portfolio risk, "
                "and risk management strategies."
            ),
            examples=[
                "What's the portfolio risk for this position?",
                "Calculate optimal position size for 1% risk",
                "What's the Value at Risk for my portfolio?"
            ]
        ),
        ExpertProfile(
            expert_type=HuiHuiExpertType.EXECUTION,
            keywords=["execution", "order execution", "slippage", "timing", "execution analysis"],
            description=(
                "Specializes in trade execution analysis, slippage minimization, "
                "and optimal execution timing strategies."
            ),
            examples=[
                "What's the best execution strategy for this order?",
                "Analyze the slippage on my recent trades",
                "When is the optimal time to execute this trade?"
            ]
        )
    ]
    
    def __init__(
        self,
        embedding_cache: Optional[UltraFastEmbeddingCache] = None,
        ollama_host: str = "http://localhost:11434",
        model_name: str = "nomic-embed-text",
        model_embedding_dimension: int = 768,
        similarity_threshold: float = 0.5,
        max_retries: int = 3,
        **kwargs
    ):
        """
        Initialize the vector-based routing strategy.
        
        Args:
            embedding_cache: Optional cache for embeddings
            ollama_host: URL of the Ollama server
            model_name: Name of the embedding model to use
            model_embedding_dimension: The dimension of the embedding model's output vector
            similarity_threshold: Minimum similarity score to consider a match
            max_retries: Maximum number of retries for embedding requests
            **kwargs: Additional arguments passed to the base class
        """
        super().__init__(strategy_name="vector_based")
        self.ollama_host = ollama_host.rstrip('/')
        self.model_name = model_name
        self.model_embedding_dimension = model_embedding_dimension
        self.similarity_threshold = similarity_threshold
        self.max_retries = max_retries
        
        # Initialize embedding cache
        self.embedding_cache = embedding_cache or UltraFastEmbeddingCache()
        
        # Initialize expert profiles
        self.expert_profiles = {}
        self.expert_embeddings = {}
        
        # Will be populated in initialize()
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize the strategy by loading expert profiles and embeddings."""
        if self._initialized:
            return
            
        self.logger.info("Initializing vector-based routing strategy")
        
        # Load default expert profiles
        for profile in self.DEFAULT_EXPERTS:
            self.expert_profiles[profile.expert_type] = profile
        
        # Pre-compute expert embeddings
        await self._precompute_expert_embeddings()
        
        self._initialized = True
        self.logger.info(f"Initialized {len(self.expert_profiles)} expert profiles")
    
    async def _get_embedding(self, text: str) -> np.ndarray:
        """
        Get the embedding for the given text, using cache if available.
        
        Args:
            text: The input text to embed
            
        Returns:
            A numpy array containing the embedding vector
        """
        # Check cache first
        cached_embedding = self.embedding_cache.get(text)
        if cached_embedding is not None:
            self.logger.debug(f"Embedding cache hit for text: '{text[:80]}...'")
            return cached_embedding
        
        self.logger.info(f"Requesting embedding for text snippet: '{text[:80]}...'")
        
        payload = {
            "model": self.model_name,
            "prompt": text
        }
        
        headers = {"Content-Type": "application/json"}
        endpoint = f"{self.ollama_host}/api/embeddings"
        
        async with aiohttp.ClientSession() as session:
            for attempt in range(self.max_retries):
                try:
                    self.logger.debug(f"Embedding request attempt {attempt + 1}/{self.max_retries}")
                    async with session.post(
                        endpoint,
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=60.0)  # Increased timeout
                    ) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            self.logger.error(
                                f"Error getting embedding (attempt {attempt + 1}/{self.max_retries}): "
                                f"{response.status} - {error_text}"
                            )
                            if attempt < self.max_retries - 1:
                                await asyncio.sleep(0.5 * (2 ** attempt))
                                continue
                            else:
                                raise RuntimeError(f"Failed to get embedding after {self.max_retries} attempts: {error_text}")
                        
                        result = await response.json()
                        embedding = np.array(result.get("embedding", []))
                        
                        # Cache the result
                        self.embedding_cache.set(text, embedding)
                        self.logger.info(f"Successfully received and cached embedding for text snippet: '{text[:80]}...'")
                        return embedding
                        
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    self.logger.error(
                        f"Network/Timeout Exception getting embedding (attempt {attempt + 1}/{self.max_retries}): {str(e)}",
                        exc_info=True
                    )
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(0.5 * (2 ** attempt))
                    else:
                        raise RuntimeError("Failed to get embedding after multiple retries due to network/timeout errors") from e
                except Exception as e:
                    self.logger.error(
                        f"Unexpected Exception getting embedding (attempt {attempt + 1}/{self.max_retries}): {str(e)}",
                        exc_info=True
                    )
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(0.5 * (2 ** attempt))
                    else:
                        raise RuntimeError("Failed to get embedding after multiple retries due to unexpected errors") from e

        # Should never reach here due to raise above
        raise RuntimeError("Failed to get embedding after multiple retries")
    
    async def _precompute_expert_embeddings(self) -> None:
        """Pre-compute embeddings for all expert profiles."""
        self.logger.info("Pre-computing expert embeddings...")
        
        for expert_type, profile in self.expert_profiles.items():
            try:
                embedding = await self._get_embedding(profile.to_embedding_text())
                self.expert_embeddings[expert_type] = embedding
                self.logger.debug(f"Computed embedding for {expert_type.value}")
            except Exception as e:
                self.logger.error(
                    f"Error computing embedding for {expert_type.value}: {str(e)}",
                    exc_info=True
                )
                # Use a zero vector as fallback
                self.expert_embeddings[expert_type] = np.zeros(self.model_embedding_dimension)
        
        self.logger.info("Finished pre-computing expert embeddings")
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """
        Compute the cosine similarity between two vectors.
        
        Args:
            a: First vector
            b: Second vector
            
        Returns:
            Cosine similarity between a and b (range: -1 to 1)
        """
        a_norm = np.linalg.norm(a)
        b_norm = np.linalg.norm(b)
        
        if a_norm == 0 or b_norm == 0:
            return 0.0
            
        return float(np.dot(a, b) / (a_norm * b_norm))
    
    async def select_expert(
        self, 
        prompt: str,
        context: Optional[Dict[str, Any]] = None
    ) -> RoutingDecision:
        """
        Select the best expert for the given prompt using vector similarity.
        
        Args:
            prompt: The input prompt to route
            context: Optional context for the request
            
        Returns:
            A RoutingDecision object with the selected expert and metadata
        """
        if not self._initialized:
            await self.initialize()
        
        # Get embedding for the input prompt
        try:
            prompt_embedding = await self._get_embedding(prompt)
        except Exception as e:
            self.logger.error(f"Error getting prompt embedding: {str(e)}", exc_info=True)
            # Fall back to orchestrator if we can't get an embedding
            return RoutingDecision(
                expert_type=HuiHuiExpertType.ORCHESTRATOR,
                confidence=0.0,
                strategy_used="fallback",
                metadata={"error": str(e), "fallback_reason": "embedding_failed"}
            )
        
        # Calculate similarity to each expert profile
        similarities = []
        for expert_type, expert_embedding in self.expert_embeddings.items():
            similarity = self._cosine_similarity(prompt_embedding, expert_embedding)
            similarities.append((expert_type, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Get the best match
        best_expert, best_score = similarities[0] if similarities else (HuiHuiExpertType.ORCHESTRATOR, 0.0)
        
        # Apply threshold and determine final expert and confidence
        if best_score < self.similarity_threshold:
            selected_expert = HuiHuiExpertType.ORCHESTRATOR
            confidence = best_score  # Pass the low score as confidence for the fallback
            fallback_reason = f"similarity_below_threshold ({best_score:.2f} < {self.similarity_threshold})"
        else:
            selected_expert = best_expert
            confidence = best_score
            fallback_reason = None
        
        # Prepare metadata
        metadata = {
            "similarity_scores": {
                expert.value: float(score) 
                for expert, score in similarities[:5]  # Top 5 for debugging
            },
            "selected_expert": selected_expert.value,
            "confidence_score": float(confidence),
            "best_match_before_fallback": {
                "expert": best_expert.value,
                "score": float(best_score)
            }
        }
        
        if fallback_reason:
            metadata["fallback_reason"] = fallback_reason
        
        self.logger.debug(
            f"Selected expert: {selected_expert.value} (confidence: {confidence:.2f})\n"
            f"Top candidates: {[(e.value, f'{s:.2f}') for e, s in similarities[:3]]}"
        )
        
        return RoutingDecision(
            expert_type=selected_expert,
            confidence=confidence,
            strategy_used=self.strategy_name,
            metadata=metadata
        )
    
    def get_strategy_state(self) -> Dict[str, Any]:
        """Get the current state of the strategy."""
        return {
            **super().get_strategy_state(),
            "model": self.model_name,
            "similarity_threshold": self.similarity_threshold,
            "experts_initialized": self._initialized,
            "num_experts": len(self.expert_profiles),
            "cache_stats": self.embedding_cache.get_stats() if hasattr(self, 'embedding_cache') else {}
        }
