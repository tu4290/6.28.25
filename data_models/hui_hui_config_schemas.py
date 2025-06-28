# hui_hui_config_schemas.py
# This module defines Pydantic models to replace Dict[str, Any] patterns in HuiHui AI system

from typing import Dict, Any, Union, List
from pydantic import BaseModel, Field
from datetime import datetime

class AnalysisContext(BaseModel):
    """Context data for HuiHui analysis requests."""
    market_conditions: str = Field(default="normal", description="Current market conditions")
    recent_news: List[str] = Field(default_factory=list, description="Recent news items")
    volatility_regime: str = Field(default="normal", description="Current volatility regime")
    market_sentiment: str = Field(default="neutral", description="Market sentiment")
    time_of_day: str = Field(default="market_hours", description="Time context")
    custom_context: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom context fields")
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

class RequestMetadata(BaseModel):
    """Metadata for HuiHui analysis requests."""
    request_id: str = Field(default="", description="Unique request identifier")
    user_id: str = Field(default="", description="User identifier")
    session_id: str = Field(default="", description="Session identifier")
    priority: str = Field(default="normal", description="Request priority")
    source: str = Field(default="api", description="Request source")
    custom_metadata: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom metadata fields")
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

class EOTSPrediction(BaseModel):
    """EOTS prediction data structure."""
    prediction_type: str = Field(description="Type of prediction")
    symbol: str = Field(description="Symbol for prediction")
    confidence: float = Field(description="Prediction confidence")
    timeframe: str = Field(description="Prediction timeframe")
    direction: str = Field(description="Predicted direction")
    target_price: float = Field(default=0.0, description="Target price if applicable")
    probability: float = Field(default=0.0, description="Probability estimate")
    custom_data: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom prediction data")
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

class TradingRecommendation(BaseModel):
    """Trading recommendation structure."""
    action: str = Field(description="Recommended action (buy/sell/hold)")
    symbol: str = Field(description="Symbol for recommendation")
    quantity: int = Field(default=0, description="Recommended quantity")
    price_target: float = Field(default=0.0, description="Price target")
    stop_loss: float = Field(default=0.0, description="Stop loss level")
    confidence: float = Field(description="Recommendation confidence")
    reasoning: str = Field(default="", description="Reasoning for recommendation")
    risk_level: str = Field(default="medium", description="Risk level")
    timeframe: str = Field(default="intraday", description="Recommendation timeframe")
    custom_attributes: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom recommendation attributes")
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

class PerformanceByCondition(BaseModel):
    """Performance metrics by market condition."""
    success_rate: float = Field(default=0.0, description="Success rate for this condition")
    avg_processing_time: float = Field(default=0.0, description="Average processing time")
    total_requests: int = Field(default=0, description="Total requests in this condition")
    avg_confidence: float = Field(default=0.0, description="Average confidence score")
    error_rate: float = Field(default=0.0, description="Error rate for this condition")
    custom_metrics: Dict[str, float] = Field(default_factory=dict, description="Custom performance metrics")
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()