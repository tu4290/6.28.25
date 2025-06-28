"""Learning configuration schemas for the Elite Options Trading System v2.5.

This module defines Pydantic models to replace Dict[str, Any] patterns in learning
and intelligence systems, providing type safety and validation.
"""
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime

class MarketContextData(BaseModel):
    """Market conditions and context relevant to learning insights."""
    market_regime: Optional[str] = Field(None, description="Current market regime")
    volatility_level: Optional[float] = Field(None, description="Current volatility level")
    trend_direction: Optional[str] = Field(None, description="Current trend direction")
    volume_profile: Optional[str] = Field(None, description="Volume profile analysis")
    sector_rotation: Optional[str] = Field(None, description="Sector rotation pattern")
    economic_indicators: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Economic indicators")
    technical_indicators: Dict[str, float] = Field(default_factory=dict, description="Technical indicator values")
    sentiment_metrics: Dict[str, float] = Field(default_factory=dict, description="Market sentiment metrics")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return self.model_dump()

class AdaptationSuggestion(BaseModel):
    """Suggested adaptation parameters based on learning insights."""
    parameter_name: Optional[str] = Field(None, description="Name of parameter to adjust")
    current_value: Optional[Union[str, int, float, bool]] = Field(None, description="Current parameter value")
    suggested_value: Optional[Union[str, int, float, bool]] = Field(None, description="Suggested new value")
    adjustment_reason: Optional[str] = Field(None, description="Reason for the adjustment")
    expected_impact: Optional[str] = Field(None, description="Expected impact of the change")
    confidence_level: Optional[float] = Field(None, description="Confidence in the suggestion")
    risk_assessment: Optional[str] = Field(None, description="Risk assessment of the change")
    rollback_plan: Optional[str] = Field(None, description="Plan for rolling back if needed")
    custom_adaptations: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom adaptation parameters")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return self.model_dump()

class PerformanceMetricsSnapshot(BaseModel):
    """Performance metrics snapshot for before/after comparisons."""
    accuracy_pct: Optional[float] = Field(None, description="Accuracy percentage")
    precision_pct: Optional[float] = Field(None, description="Precision percentage")
    recall_pct: Optional[float] = Field(None, description="Recall percentage")
    f1_score: Optional[float] = Field(None, description="F1 score")
    sharpe_ratio: Optional[float] = Field(None, description="Sharpe ratio")
    max_drawdown_pct: Optional[float] = Field(None, description="Maximum drawdown percentage")
    win_rate_pct: Optional[float] = Field(None, description="Win rate percentage")
    profit_factor: Optional[float] = Field(None, description="Profit factor")
    avg_return_pct: Optional[float] = Field(None, description="Average return percentage")
    volatility_pct: Optional[float] = Field(None, description="Volatility percentage")
    execution_time_ms: Optional[float] = Field(None, description="Average execution time in milliseconds")
    resource_usage_pct: Optional[float] = Field(None, description="Resource usage percentage")
    custom_metrics: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom performance metrics")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return self.model_dump()

class LearningInsightData(BaseModel):
    """Summarized learning insights from analysis."""
    insight_category: Optional[str] = Field(None, description="Category of insights")
    key_findings: List[str] = Field(default_factory=list, description="Key findings from analysis")
    pattern_discoveries: List[str] = Field(default_factory=list, description="New patterns discovered")
    anomaly_detections: List[str] = Field(default_factory=list, description="Anomalies detected")
    correlation_insights: Dict[str, float] = Field(default_factory=dict, description="Correlation insights")
    trend_analysis: Dict[str, str] = Field(default_factory=dict, description="Trend analysis results")
    predictive_signals: List[str] = Field(default_factory=list, description="Predictive signals identified")
    confidence_evolution: Dict[str, float] = Field(default_factory=dict, description="Evolution of confidence scores")
    learning_velocity: Optional[float] = Field(None, description="Rate of learning improvement")
    custom_insights: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom insight data")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return self.model_dump()

class ExpertAdaptationSummary(BaseModel):
    """Summary of adaptations made by expert systems."""
    expert_id: Optional[str] = Field(None, description="Expert system identifier")
    adaptation_type: Optional[str] = Field(None, description="Type of adaptation performed")
    parameters_changed: List[str] = Field(default_factory=list, description="Parameters that were changed")
    performance_impact: Optional[float] = Field(None, description="Performance impact of adaptations")
    adaptation_timestamp: Optional[datetime] = Field(None, description="When adaptation was applied")
    rollback_available: Optional[bool] = Field(None, description="Whether rollback is available")
    validation_status: Optional[str] = Field(None, description="Validation status of adaptation")
    expert_confidence: Optional[float] = Field(None, description="Expert's confidence in adaptation")
    custom_adaptations: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom adaptation data")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return self.model_dump()

class ConfidenceUpdateData(BaseModel):
    """Updates on confidence scores over time."""
    metric_name: Optional[str] = Field(None, description="Name of the confidence metric")
    previous_score: Optional[float] = Field(None, description="Previous confidence score")
    current_score: Optional[float] = Field(None, description="Current confidence score")
    score_change: Optional[float] = Field(None, description="Change in confidence score")
    update_reason: Optional[str] = Field(None, description="Reason for confidence update")
    validation_data: Dict[str, float] = Field(default_factory=dict, description="Validation data supporting the update")
    trend_direction: Optional[str] = Field(None, description="Trend direction of confidence")
    stability_score: Optional[float] = Field(None, description="Stability of confidence score")
    custom_confidence_data: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom confidence data")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return self.model_dump()

class OptimizationRecommendation(BaseModel):
    """Specific recommendations for further optimization."""
    recommendation_id: Optional[str] = Field(None, description="Unique recommendation identifier")
    recommendation_type: Optional[str] = Field(None, description="Type of optimization recommendation")
    priority_level: Optional[int] = Field(None, description="Priority level (1-10)")
    description: Optional[str] = Field(None, description="Detailed description of recommendation")
    expected_benefit: Optional[str] = Field(None, description="Expected benefit from implementation")
    implementation_effort: Optional[str] = Field(None, description="Effort required for implementation")
    risk_level: Optional[str] = Field(None, description="Risk level of implementation")
    dependencies: List[str] = Field(default_factory=list, description="Dependencies for implementation")
    success_metrics: List[str] = Field(default_factory=list, description="Metrics to measure success")
    timeline_estimate: Optional[str] = Field(None, description="Estimated timeline for implementation")
    custom_recommendation_data: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom recommendation data")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return self.model_dump()

class LearningMetadata(BaseModel):
    """Additional metadata about the learning process."""
    learning_algorithm: Optional[str] = Field(None, description="Learning algorithm used")
    data_sources: List[str] = Field(default_factory=list, description="Data sources used for learning")
    training_duration_ms: Optional[float] = Field(None, description="Training duration in milliseconds")
    model_version: Optional[str] = Field(None, description="Model version used")
    feature_count: Optional[int] = Field(None, description="Number of features used")
    sample_size: Optional[int] = Field(None, description="Sample size for training")
    validation_method: Optional[str] = Field(None, description="Validation method used")
    hyperparameters: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Hyperparameters used")
    performance_benchmarks: Dict[str, float] = Field(default_factory=dict, description="Performance benchmarks")
    custom_metadata: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom learning metadata")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return self.model_dump()

class IntelligenceLayerData(BaseModel):
    """Data for intelligence analysis layers."""
    layer_id: Optional[str] = Field(None, description="Layer identifier")
    layer_type: Optional[str] = Field(None, description="Type of intelligence layer")
    analysis_depth: Optional[int] = Field(None, description="Depth of analysis")
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")
    confidence_score: Optional[float] = Field(None, description="Layer confidence score")
    insights_generated: List[str] = Field(default_factory=list, description="Insights generated by this layer")
    data_quality_score: Optional[float] = Field(None, description="Quality score of input data")
    convergence_metrics: Dict[str, float] = Field(default_factory=dict, description="Convergence metrics")
    layer_dependencies: List[str] = Field(default_factory=list, description="Dependencies on other layers")
    custom_layer_data: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom layer data")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return self.model_dump()

class MetaLearningData(BaseModel):
    """Meta-learning information for recursive intelligence."""
    meta_algorithm: Optional[str] = Field(None, description="Meta-learning algorithm used")
    learning_rate: Optional[float] = Field(None, description="Learning rate")
    adaptation_speed: Optional[float] = Field(None, description="Speed of adaptation")
    transfer_learning_score: Optional[float] = Field(None, description="Transfer learning effectiveness")
    generalization_ability: Optional[float] = Field(None, description="Generalization ability score")
    meta_features: Dict[str, float] = Field(default_factory=dict, description="Meta-features extracted")
    learning_trajectory: List[float] = Field(default_factory=list, description="Learning trajectory over time")
    convergence_history: List[float] = Field(default_factory=list, description="Convergence history")
    meta_insights: List[str] = Field(default_factory=list, description="Meta-learning insights")
    custom_meta_data: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom meta-learning data")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return self.model_dump()

class PatternFeatures(BaseModel):
    """Key features of detected patterns."""
    feature_type: Optional[str] = Field(None, description="Type of pattern feature")
    feature_importance: Optional[float] = Field(None, description="Importance score of the feature")
    feature_stability: Optional[float] = Field(None, description="Stability of the feature")
    temporal_characteristics: Dict[str, float] = Field(default_factory=dict, description="Temporal characteristics")
    statistical_properties: Dict[str, float] = Field(default_factory=dict, description="Statistical properties")
    correlation_matrix: Dict[str, float] = Field(default_factory=dict, description="Feature correlations")
    anomaly_scores: Dict[str, float] = Field(default_factory=dict, description="Anomaly detection scores")
    feature_evolution: List[float] = Field(default_factory=list, description="Evolution of feature over time")
    custom_features: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom pattern features")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return self.model_dump()

class MarketPrediction(BaseModel):
    """Pattern-based market prediction."""
    prediction_type: Optional[str] = Field(None, description="Type of prediction")
    prediction_horizon: Optional[str] = Field(None, description="Time horizon for prediction")
    predicted_direction: Optional[str] = Field(None, description="Predicted market direction")
    confidence_level: Optional[float] = Field(None, description="Confidence in prediction")
    probability_estimates: Dict[str, float] = Field(default_factory=dict, description="Probability estimates")
    risk_assessment: Dict[str, float] = Field(default_factory=dict, description="Risk assessment")
    supporting_evidence: List[str] = Field(default_factory=list, description="Supporting evidence for prediction")
    alternative_scenarios: List[str] = Field(default_factory=list, description="Alternative scenarios")
    validation_criteria: List[str] = Field(default_factory=list, description="Criteria for validating prediction")
    custom_prediction_data: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom prediction data")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return self.model_dump()

class PatternMetaAnalysis(BaseModel):
    """Meta-analysis of detected patterns."""
    analysis_method: Optional[str] = Field(None, description="Meta-analysis method used")
    pattern_frequency: Optional[float] = Field(None, description="Frequency of pattern occurrence")
    seasonal_patterns: Dict[str, float] = Field(default_factory=dict, description="Seasonal pattern analysis")
    market_regime_dependency: Dict[str, float] = Field(default_factory=dict, description="Dependency on market regimes")
    cross_asset_correlations: Dict[str, float] = Field(default_factory=dict, description="Cross-asset correlations")
    pattern_evolution: List[float] = Field(default_factory=list, description="Evolution of pattern over time")
    robustness_metrics: Dict[str, float] = Field(default_factory=dict, description="Pattern robustness metrics")
    sensitivity_analysis: Dict[str, float] = Field(default_factory=dict, description="Sensitivity analysis results")
    meta_insights: List[str] = Field(default_factory=list, description="Meta-analysis insights")
    custom_meta_analysis: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Custom meta-analysis data")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backward compatibility."""
        return self.model_dump()