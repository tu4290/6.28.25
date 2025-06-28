"""
Data Models for EOTS v2.5

This package contains all Pydantic models used throughout the system,
organized into logical submodules.

This __init__.py file exposes the most commonly used models for easy access.
"""

from .advanced_metrics import AdvancedOptionsMetricsV2_5
from .ai_adaptations import AIAdaptationV2_5, AIAdaptationPerformanceV2_5
from .ai_predictions import AIPredictionV2_5, AIPredictionPerformanceV2_5, AIPredictionRequestV2_5
from .atif_schemas import (
    ATIFSituationalAssessmentProfileV2_5,
    ATIFStrategyDirectivePayloadV2_5,
    ATIFManagementDirectiveV2_5,
)
from .base_types import PandasDataFrame, DataFrameSchema
from .bundle_schemas import FinalAnalysisBundleV2_5
from .configuration_schemas import (
    EOTSConfigV2_5,
    AnalyticsEngineConfigV2_5,
    AdaptiveLearningConfigV2_5,
    MarketRegimeEngineSettings
)
from .context_schemas import TickerContextDictV2_5, MarketRegimeState, TimeOfDayDefinitions
from .dashboard_schemas import (
    DashboardModeType,
    ChartType,
    DashboardModeUIDetail,
    ChartLayoutConfigV2_5,
    ControlPanelParametersV2_5,
    DashboardConfigV2_5,
    ComponentComplianceV2_5,
    DashboardStateV2_5,
)
from .hui_hui_schemas import (
    HuiHuiExpertType,
    HuiHuiModelConfigV2_5,
    HuiHuiExpertConfigV2_5,
    HuiHuiAnalysisRequestV2_5,
    HuiHuiAnalysisResponseV2_5,
    HuiHuiUsageRecordV2_5,
    HuiHuiPerformanceMetricsV2_5,
    HuiHuiEnsembleConfigV2_5,
    HuiHuiUserFeedbackV2_5,
)
from .learning_schemas import LearningInsightV2_5, UnifiedLearningResult # New import
from .moe_schemas_v2_5 import (
    ExpertStatus,
    RoutingStrategy,
    ConsensusStrategy,
    AgreementLevel,
    HealthStatus,
    MOEExpertRegistryV2_5,
    MOEGatingNetworkV2_5,
    MOEExpertResponseV2_5,
    MOEUnifiedResponseV2_5,
)
from .performance_schemas import (
    PerformanceInterval,
    PerformanceMetricType,
    PerformanceMetricV2_5,
    SystemPerformanceV2_5,
    BacktestPerformanceV2_5,
    ExecutionMetricsV2_5,
    PerformanceReportV2_5,
)
from .processed_data import (
    ProcessedContractMetricsV2_5,
    ProcessedStrikeLevelMetricsV2_5,
    ProcessedUnderlyingAggregatesV2_5,
    ProcessedDataBundleV2_5,
)
from .raw_data import (
    RawOptionsContractV2_5,
    RawUnderlyingDataV2_5,
    RawUnderlyingDataCombinedV2_5,
    UnprocessedDataBundleV2_5,
)
from .recommendation_schemas import TradeParametersV2_5, ActiveRecommendationPayloadV2_5
from .signal_level_schemas import SignalPayloadV2_5, KeyLevelV2_5, KeyLevelsDataV2_5

__all__ = [
    # advanced_metrics
    "AdvancedOptionsMetricsV2_5",
    # ai_adaptations
    "AIAdaptationV2_5",
    "AIAdaptationPerformanceV2_5",
    # ai_predictions
    "AIPredictionV2_5",
    "AIPredictionPerformanceV2_5",
    "AIPredictionRequestV2_5",
    # atif_schemas
    "ATIFSituationalAssessmentProfileV2_5",
    "ATIFStrategyDirectivePayloadV2_5",
    "ATIFManagementDirectiveV2_5",
    # base_types
    "PandasDataFrame",
    "DataFrameSchema",
    # bundle_schemas
    "FinalAnalysisBundleV2_5",
    # configuration_schemas
    "EOTSConfigV2_5",
    "AnalyticsEngineConfigV2_5",
    "AdaptiveLearningConfigV2_5",
    "MarketRegimeEngineSettings",
    # context_schemas
    "TickerContextDictV2_5",
    "MarketRegimeState",
    "TimeOfDayDefinitions",
    # dashboard_schemas
    "DashboardModeType",
    "ChartType",
    "DashboardModeUIDetail",
    "ChartLayoutConfigV2_5",
    "ControlPanelParametersV2_5",
    "DashboardConfigV2_5",
    "ComponentComplianceV2_5",
    "DashboardStateV2_5",
    # hui_hui_schemas
    "HuiHuiExpertType",
    "HuiHuiModelConfigV2_5",
    "HuiHuiExpertConfigV2_5",
    "HuiHuiAnalysisRequestV2_5",
    "HuiHuiAnalysisResponseV2_5",
    "HuiHuiUsageRecordV2_5",
    "HuiHuiPerformanceMetricsV2_5",
    "HuiHuiEnsembleConfigV2_5",
    "HuiHuiUserFeedbackV2_5",
    # learning_schemas # New section
    "LearningInsightV2_5",
    "UnifiedLearningResult",
    # moe_schemas_v2_5
    "ExpertStatus",
    "RoutingStrategy",
    "ConsensusStrategy",
    "AgreementLevel",
    "HealthStatus",
    "MOEExpertRegistryV2_5",
    "MOEGatingNetworkV2_5",
    "MOEExpertResponseV2_5",
    "MOEUnifiedResponseV2_5",
    # performance_schemas
    "PerformanceInterval",
    "PerformanceMetricType",
    "PerformanceMetricV2_5",
    "SystemPerformanceV2_5",
    "BacktestPerformanceV2_5",
    "ExecutionMetricsV2_5",
    "PerformanceReportV2_5",
    # processed_data
    "ProcessedContractMetricsV2_5",
    "ProcessedStrikeLevelMetricsV2_5",
    "ProcessedUnderlyingAggregatesV2_5",
    "ProcessedDataBundleV2_5",
    # raw_data
    "RawOptionsContractV2_5",
    "RawUnderlyingDataV2_5",
    "RawUnderlyingDataCombinedV2_5",
    "UnprocessedDataBundleV2_5",
    # recommendation_schemas
    "TradeParametersV2_5",
    "ActiveRecommendationPayloadV2_5",
    # signal_level_schemas
    "SignalPayloadV2_5",
    "KeyLevelV2_5",
    "KeyLevelsDataV2_5",
]