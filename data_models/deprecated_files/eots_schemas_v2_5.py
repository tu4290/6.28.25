"""DEPRECATED: Migration file for eots_schemas_v2_5.py

This file provides backward compatibility for imports from the old eots_schemas_v2_5.py module.
All models have been moved to more specialized modules in the data_models package.
"""
import warnings
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict

# Re-export from the new package structure
from ..base_types import PandasDataFrame

# Re-export models from the new structure
from ..raw_data import (
    RawOptionsContractV2_5,
    UnprocessedDataBundleV2_5
)

from ..processed_data import (
    ProcessedUnderlyingAggregatesV2_5,
    ProcessedContractMetricsV2_5,
    ProcessedStrikeLevelMetricsV2_5
)

from ..bundle_schemas import FinalAnalysisBundleV2_5
from ..configuration_schemas import ControlPanelParametersV2_5
from ..dashboard_schemas import ChartLayoutConfigV2_5

# Issue deprecation warning
warnings.warn(
    "eots_schemas_v2_5.py is deprecated and will be removed in a future version. "
    "Please update your imports to use the new module structure.",
    DeprecationWarning,
    stacklevel=2
)

# Placeholder for any models that might not have direct replacements
class PlaceholderModel(BaseModel):
    """Placeholder for models that might not have direct replacements."""
    pass

# Add any other commonly used models from the old schema
# You can add more re-exports or placeholders as needed 