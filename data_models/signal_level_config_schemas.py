# signal_level_config_schemas.py
# This module defines Pydantic models to replace Dict[str, Any] patterns in signal level schemas

from typing import Dict, Any, Union
from pydantic import BaseModel, Field

class SupportingMetrics(BaseModel):
    """Supporting metrics that contributed to triggering a signal."""
    vapi_fa_score: float = Field(default=0.0, description="VAPI FA score")
    a_mspi_score: float = Field(default=0.0, description="A-MSPI score")
    flow_divergence: float = Field(default=0.0, description="Flow divergence metric")
    volatility_spike: float = Field(default=0.0, description="Volatility spike indicator")
    momentum_strength: float = Field(default=0.0, description="Momentum strength")
    regime_confidence: float = Field(default=0.0, description="Regime confidence level")
    structural_support: float = Field(default=0.0, description="Structural support level")
    volume_confirmation: float = Field(default=0.0, description="Volume confirmation")
    price_action_quality: float = Field(default=0.0, description="Price action quality")
    time_decay_factor: float = Field(default=0.0, description="Time decay factor")
    custom_metrics: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom supporting metrics")
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()