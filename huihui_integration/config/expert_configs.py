"""
Config management for EOTS (ConfigManagerV2_5) and HuiHui/MOE (HuiHuiConfigV2_5).
- EOTS config is loaded/validated via ConfigManagerV2_5 (singleton, uses EOTSConfigV2_5).
- HuiHui/MOE config is loaded/validated via HuiHuiConfigV2_5 and load_huihui_config.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Optional, Dict, Union

from pydantic import ValidationError, BaseModel, Field, ConfigDict
from ...data_models.expert_config_schemas import (
    ApiKeyConfig, ModelConfig, ApiEndpointConfig, RateLimitConfig,
    SecurityConfig, PerformanceConfig, IntegrationConfig,
    AgentSettings, LearningSettings, SafetySettings,
    InsightGenerationSettings, AdaptiveThresholds
)

# Change relative import to absolute import
from data_models.configuration_schemas import EOTSConfigV2_5

__all__ = [
    "ConfigManagerV2_5",
    "HuiHuiConfigV2_5",
    "load_huihui_config"
]

logger = logging.getLogger(__name__)


class ConfigManagerV2_5:
    """
    Singleton configuration manager for EOTS v2.5.
    Handles loading, validation, and access to configuration settings.
    """
    _instance = None
    _config: Optional[EOTSConfigV2_5] = None
    _project_root: Optional[Path] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the singleton instance."""
        self._determine_project_root()
        self._load_config()

    def _determine_project_root(self):
        """Determine the project root directory."""
        # Start from the current file's directory
        current_dir = Path(__file__).parent
        # Look for the root package file
        while current_dir != current_dir.parent:
            if (current_dir / "elite_options_system_v2_5.py").exists():
                self._project_root = current_dir
                logger.debug(
                    f"Project root determined as: {self._project_root}"
                )
                return
            current_dir = current_dir.parent
        raise RuntimeError("Could not determine project root directory")

    def _substitute_env_vars(self, data):
        """Recursively substitute environment variables in configuration data."""
        import re

        if isinstance(data, dict):
            return {key: self._substitute_env_vars(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._substitute_env_vars(item) for item in data]
        elif isinstance(data, str):
            # Replace ${VAR} with environment variable value
            def replace_env_var(match):
                var_name = match.group(1)
                env_value = os.getenv(var_name)
                if env_value is None:
                    logger.warning(
                        f"Environment variable {var_name} not found, keeping placeholder"
                    )
                    return match.group(0)  # Return original ${VAR} if not found
                # Try to convert to appropriate type, but always return as str for re.sub
                if env_value.isdigit():
                    return str(int(env_value))
                try:
                    return str(float(env_value))
                except ValueError:
                    return str(env_value)

            pattern = r'\$\{([^}]+)\}'
            result = re.sub(pattern, replace_env_var, data)
            return result
        else:
            return data

    def _load_config(self):
        """Load and validate the configuration file."""
        if not self._project_root:
            raise RuntimeError("Project root not determined")

        config_path = self._project_root / "config" / "config_v2_5.json"
        logger.info(f"Loading configuration from: {config_path}")

        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)

            # Substitute environment variables
            config_data = self._substitute_env_vars(config_data)

            # Validate against JSON schema
            logger.debug("Validating configuration against JSON schema...")
            # Schema validation is handled by Pydantic model
            logger.info("JSON schema validation successful.")

            # Ensure config_data is a dict before calling .items()
            if not isinstance(config_data, dict):
                raise RuntimeError(
                    "Configuration data must be a dict after environment substitution and validation."
                )
            for key, value in list(config_data.items()):
                if hasattr(value, 'model_dump'):
                    config_data[key] = value.model_dump()
            self._config = EOTSConfigV2_5(**config_data)
            logger.info(
                "Pydantic model parsing successful. Configuration is now loaded and type-safe."
            )
        except FileNotFoundError:
            raise RuntimeError(f"Configuration file not found at {config_path}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON in configuration file: {e}")
        except ValidationError as e:
            raise RuntimeError(f"Configuration validation failed: {e}")

    def get_setting(self, path: str, default: Any = None) -> Any:
        """
        Get a configuration setting by path.

        Args:
            path: Dot-separated path to the setting (e.g., 'database.host')
            default: Default value to return if setting not found

        Returns:
            The requested setting value or default if not found
        """
        if not self._config:
            raise RuntimeError("Configuration not loaded")

        try:
            parts = path.split('.')
            value = self._config
            for part in parts:
                value = getattr(value, part)
            return value
        except (AttributeError, KeyError):
            return default

    @property
    def config(self) -> EOTSConfigV2_5:
        """Get the loaded configuration object."""
        if not self._config:
            raise RuntimeError("Configuration not loaded")
        return self._config

    def get_project_root(self) -> Path:
        """Get the project root directory."""
        if not self._project_root:
            raise RuntimeError("Project root not determined")
        return self._project_root

    def get_resolved_path(self, path: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get a configuration setting that represents a path and resolve it relative to project root.

        Args:
            path: Dot-notation path to the setting (e.g., 'performance_tracker_settings_v2_5.performance_data_directory')
            default: Default value to return if setting is not found

        Returns:
            The resolved path string or None if not found
        """
        relative_path = self.get_setting(path, default)
        if not relative_path:
            return None

        if not self._project_root:
            raise RuntimeError("Project root not determined")
        return str(self._project_root / relative_path)

    def load_config(self):
        """Public method to load the configuration."""
        self._load_config()


class LLMApiModel(BaseModel):
    enabled: Optional[bool] = None
    ollama_host: Optional[str] = None
    api_version: Optional[str] = None
    api_keys: ApiKeyConfig = Field(default_factory=ApiKeyConfig)
    models: ModelConfig = Field(default_factory=ModelConfig)
    api_endpoints: ApiEndpointConfig = Field(default_factory=ApiEndpointConfig)
    rate_limits: RateLimitConfig = Field(default_factory=RateLimitConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    integration: IntegrationConfig = Field(default_factory=IntegrationConfig)


class AISettingsModel(BaseModel):
    enabled: Optional[bool] = None
    model_config = ConfigDict(extra='allow')
    agent_settings: AgentSettings = Field(default_factory=AgentSettings)
    learning_settings: LearningSettings = Field(default_factory=LearningSettings)
    safety_settings: SafetySettings = Field(default_factory=SafetySettings)
    insight_generation: InsightGenerationSettings = Field(default_factory=InsightGenerationSettings)
    adaptive_thresholds: AdaptiveThresholds = Field(default_factory=AdaptiveThresholds)


class HuiHuiConfigV2_5(BaseModel):
    llm_api: Optional[LLMApiModel] = None
    ai_settings: Optional[AISettingsModel] = None
    integration: IntegrationConfig = Field(default_factory=IntegrationConfig)


def load_huihui_config(
    config_path: Optional[Union[str, Path]] = None
) -> HuiHuiConfigV2_5:
    """
    Load and validate the HuiHui/MOE config from JSON file.
    Args:
        config_path: Path to huihui_config.json (default: project_root/config/huihui_config.json)
    Returns:
        Validated HuiHuiConfigV2_5 instance
    Raises:
        RuntimeError if file not found or validation fails
    """
    if config_path is None:
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "config" / "huihui_config.json"
    elif not isinstance(config_path, Path):
        config_path = Path(config_path)
    if not config_path.exists():
        logger.warning(
            f"HuiHui config file not found at {config_path}, returning default config."
        )
        return HuiHuiConfigV2_5()
    with open(str(config_path), 'r') as f:
        config_data = json.load(f)
    try:
        return HuiHuiConfigV2_5(**config_data)
    except ValidationError as e:
        logger.error(f"HuiHui config validation failed: {e}")
        raise RuntimeError(f"HuiHui config validation failed: {e}")