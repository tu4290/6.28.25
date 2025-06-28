"""Detailed configuration schemas for expert system components.

This module defines Pydantic models to replace Dict[str, Any] patterns
in expert configuration schemas, providing better type safety and validation.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class CustomApiKeys(BaseModel):
    """Custom API key configurations."""
    openai_key: Optional[str] = Field(None, description="OpenAI API key")
    anthropic_key: Optional[str] = Field(None, description="Anthropic API key")
    google_key: Optional[str] = Field(None, description="Google API key")
    azure_key: Optional[str] = Field(None, description="Azure API key")
    custom_provider_keys: Dict[str, str] = Field(default_factory=dict, description="Additional provider keys")
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary format for backward compatibility."""
        result = {}
        if self.openai_key:
            result["openai"] = self.openai_key
        if self.anthropic_key:
            result["anthropic"] = self.anthropic_key
        if self.google_key:
            result["google"] = self.google_key
        if self.azure_key:
            result["azure"] = self.azure_key
        result.update(self.custom_provider_keys)
        return result


class CustomModelConfig(BaseModel):
    """Custom model configuration details."""
    model_name: str = Field(..., description="Name of the custom model")
    provider: str = Field(..., description="Model provider")
    endpoint_url: Optional[str] = Field(None, description="Custom endpoint URL")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens for this model")
    temperature: Optional[float] = Field(None, description="Temperature setting for this model")
    cost_per_token: Optional[float] = Field(None, description="Cost per token for this model")
    capabilities: Dict[str, bool] = Field(default_factory=dict, description="Model capabilities")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for backward compatibility."""
        return {
            "name": self.model_name,
            "provider": self.provider,
            "endpoint": self.endpoint_url,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "cost_per_token": self.cost_per_token,
            "capabilities": self.capabilities
        }


class CustomEndpoints(BaseModel):
    """Custom API endpoint configurations."""
    chat_endpoint: Optional[str] = Field(None, description="Custom chat endpoint")
    embeddings_endpoint: Optional[str] = Field(None, description="Custom embeddings endpoint")
    completion_endpoint: Optional[str] = Field(None, description="Custom completion endpoint")
    streaming_endpoint: Optional[str] = Field(None, description="Custom streaming endpoint")
    additional_endpoints: Dict[str, str] = Field(default_factory=dict, description="Additional custom endpoints")
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary format for backward compatibility."""
        result = {}
        if self.chat_endpoint:
            result["chat"] = self.chat_endpoint
        if self.embeddings_endpoint:
            result["embeddings"] = self.embeddings_endpoint
        if self.completion_endpoint:
            result["completion"] = self.completion_endpoint
        if self.streaming_endpoint:
            result["streaming"] = self.streaming_endpoint
        result.update(self.additional_endpoints)
        return result


class CustomRateLimits(BaseModel):
    """Custom rate limit configurations."""
    requests_per_minute: Optional[int] = Field(None, description="Custom requests per minute")
    tokens_per_minute: Optional[int] = Field(None, description="Custom tokens per minute")
    concurrent_requests: Optional[int] = Field(None, description="Custom concurrent requests limit")
    burst_limit: Optional[int] = Field(None, description="Burst limit for requests")
    provider_limits: Dict[str, int] = Field(default_factory=dict, description="Provider-specific limits")
    
    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary format for backward compatibility."""
        result = {}
        if self.requests_per_minute:
            result["rpm"] = self.requests_per_minute
        if self.tokens_per_minute:
            result["tpm"] = self.tokens_per_minute
        if self.concurrent_requests:
            result["concurrent"] = self.concurrent_requests
        if self.burst_limit:
            result["burst"] = self.burst_limit
        result.update(self.provider_limits)
        return result


class CustomSecuritySettings(BaseModel):
    """Custom security configuration settings."""
    encryption_algorithm: Optional[str] = Field(None, description="Encryption algorithm to use")
    key_rotation_interval: Optional[int] = Field(None, description="Key rotation interval in hours")
    access_control_enabled: Optional[bool] = Field(None, description="Whether access control is enabled")
    audit_logging: Optional[bool] = Field(None, description="Whether audit logging is enabled")
    ip_whitelist: Optional[list] = Field(None, description="IP whitelist for access")
    security_headers: Dict[str, str] = Field(default_factory=dict, description="Custom security headers")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for backward compatibility."""
        return {
            "encryption": self.encryption_algorithm,
            "key_rotation": self.key_rotation_interval,
            "access_control": self.access_control_enabled,
            "audit_logging": self.audit_logging,
            "ip_whitelist": self.ip_whitelist,
            "headers": self.security_headers
        }


class CustomPerformanceSettings(BaseModel):
    """Custom performance configuration settings."""
    connection_pool_size: Optional[int] = Field(None, description="Connection pool size")
    request_timeout: Optional[int] = Field(None, description="Request timeout in seconds")
    retry_strategy: Optional[str] = Field(None, description="Retry strategy to use")
    circuit_breaker_enabled: Optional[bool] = Field(None, description="Whether circuit breaker is enabled")
    load_balancing_strategy: Optional[str] = Field(None, description="Load balancing strategy")
    performance_metrics: Dict[str, Any] = Field(default_factory=dict, description="Performance metrics configuration")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for backward compatibility."""
        return {
            "pool_size": self.connection_pool_size,
            "timeout": self.request_timeout,
            "retry_strategy": self.retry_strategy,
            "circuit_breaker": self.circuit_breaker_enabled,
            "load_balancing": self.load_balancing_strategy,
            "metrics": self.performance_metrics
        }


class CustomIntegrationSettings(BaseModel):
    """Custom integration configuration settings."""
    webhook_retries: Optional[int] = Field(None, description="Number of webhook retries")
    webhook_timeout: Optional[int] = Field(None, description="Webhook timeout in seconds")
    database_connection_string: Optional[str] = Field(None, description="Custom database connection")
    monitoring_endpoints: Optional[list] = Field(None, description="Monitoring endpoints")
    notification_channels: Optional[list] = Field(None, description="Notification channels")
    integration_configs: Dict[str, Any] = Field(default_factory=dict, description="Integration-specific configs")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for backward compatibility."""
        return {
            "webhook_retries": self.webhook_retries,
            "webhook_timeout": self.webhook_timeout,
            "database": self.database_connection_string,
            "monitoring": self.monitoring_endpoints,
            "notifications": self.notification_channels,
            "configs": self.integration_configs
        }


class CustomAgentSettings(BaseModel):
    """Custom agent configuration settings."""
    reasoning_strategy: Optional[str] = Field(None, description="Reasoning strategy to use")
    memory_persistence: Optional[bool] = Field(None, description="Whether to persist memory")
    context_compression: Optional[bool] = Field(None, description="Whether to compress context")
    multi_agent_coordination: Optional[bool] = Field(None, description="Multi-agent coordination enabled")
    tool_usage_limits: Optional[dict] = Field(None, description="Tool usage limits")
    agent_behaviors: Dict[str, Any] = Field(default_factory=dict, description="Agent behavior configurations")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for backward compatibility."""
        return {
            "reasoning": self.reasoning_strategy,
            "memory_persistence": self.memory_persistence,
            "context_compression": self.context_compression,
            "multi_agent": self.multi_agent_coordination,
            "tool_limits": self.tool_usage_limits,
            "behaviors": self.agent_behaviors
        }


class CustomLearningSettings(BaseModel):
    """Custom learning configuration settings."""
    learning_algorithm: Optional[str] = Field(None, description="Learning algorithm to use")
    data_retention_period: Optional[int] = Field(None, description="Data retention period in days")
    model_versioning: Optional[bool] = Field(None, description="Whether to version models")
    continuous_learning: Optional[bool] = Field(None, description="Continuous learning enabled")
    feedback_processing: Optional[str] = Field(None, description="Feedback processing strategy")
    learning_configs: Dict[str, Any] = Field(default_factory=dict, description="Learning-specific configurations")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for backward compatibility."""
        return {
            "algorithm": self.learning_algorithm,
            "retention": self.data_retention_period,
            "versioning": self.model_versioning,
            "continuous": self.continuous_learning,
            "feedback": self.feedback_processing,
            "configs": self.learning_configs
        }


class CustomSafetySettings(BaseModel):
    """Custom safety configuration settings."""
    content_moderation_level: Optional[str] = Field(None, description="Content moderation level")
    bias_detection_enabled: Optional[bool] = Field(None, description="Bias detection enabled")
    harmful_content_filters: Optional[list] = Field(None, description="Harmful content filters")
    safety_escalation_rules: Optional[dict] = Field(None, description="Safety escalation rules")
    compliance_standards: Optional[list] = Field(None, description="Compliance standards to follow")
    safety_configs: Dict[str, Any] = Field(default_factory=dict, description="Safety-specific configurations")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for backward compatibility."""
        return {
            "moderation_level": self.content_moderation_level,
            "bias_detection": self.bias_detection_enabled,
            "content_filters": self.harmful_content_filters,
            "escalation_rules": self.safety_escalation_rules,
            "compliance": self.compliance_standards,
            "configs": self.safety_configs
        }


class CustomInsightSettings(BaseModel):
    """Custom insight generation settings."""
    insight_algorithms: Optional[list] = Field(None, description="Insight generation algorithms")
    data_sources: Optional[list] = Field(None, description="Data sources for insights")
    insight_validation: Optional[bool] = Field(None, description="Insight validation enabled")
    real_time_insights: Optional[bool] = Field(None, description="Real-time insight generation")
    insight_storage: Optional[str] = Field(None, description="Insight storage strategy")
    insight_configs: Dict[str, Any] = Field(default_factory=dict, description="Insight-specific configurations")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for backward compatibility."""
        return {
            "algorithms": self.insight_algorithms,
            "data_sources": self.data_sources,
            "validation": self.insight_validation,
            "real_time": self.real_time_insights,
            "storage": self.insight_storage,
            "configs": self.insight_configs
        }


class ThresholdTypes(BaseModel):
    """Different threshold type configurations."""
    confidence_threshold: Optional[float] = Field(None, description="Confidence threshold")
    accuracy_threshold: Optional[float] = Field(None, description="Accuracy threshold")
    performance_threshold: Optional[float] = Field(None, description="Performance threshold")
    quality_threshold: Optional[float] = Field(None, description="Quality threshold")
    risk_threshold: Optional[float] = Field(None, description="Risk threshold")
    additional_thresholds: Dict[str, float] = Field(default_factory=dict, description="Additional threshold types")
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary format for backward compatibility."""
        result = {}
        if self.confidence_threshold is not None:
            result["confidence"] = self.confidence_threshold
        if self.accuracy_threshold is not None:
            result["accuracy"] = self.accuracy_threshold
        if self.performance_threshold is not None:
            result["performance"] = self.performance_threshold
        if self.quality_threshold is not None:
            result["quality"] = self.quality_threshold
        if self.risk_threshold is not None:
            result["risk"] = self.risk_threshold
        result.update(self.additional_thresholds)
        return result


class CustomThresholdSettings(BaseModel):
    """Custom threshold configuration settings."""
    dynamic_adjustment: Optional[bool] = Field(None, description="Dynamic threshold adjustment")
    adjustment_frequency: Optional[int] = Field(None, description="Adjustment frequency in minutes")
    threshold_history: Optional[bool] = Field(None, description="Keep threshold history")
    threshold_alerts: Optional[bool] = Field(None, description="Threshold breach alerts")
    threshold_validation: Optional[str] = Field(None, description="Threshold validation strategy")
    threshold_configs: Dict[str, Any] = Field(default_factory=dict, description="Threshold-specific configurations")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for backward compatibility."""
        return {
            "dynamic": self.dynamic_adjustment,
            "frequency": self.adjustment_frequency,
            "history": self.threshold_history,
            "alerts": self.threshold_alerts,
            "validation": self.threshold_validation,
            "configs": self.threshold_configs
        }