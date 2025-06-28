# EOTS Schema Migration Notes (v2.5)

## Overview
The monolithic `eots_schemas_v2_5.py` has been deprecated and refactored into multiple specialized schema files.

## Migration Strategy
- Schemas have been distributed across multiple files in the `data_models/` directory
- Key models have been ported to:
  - `processed_data.py`
  - `configuration_schemas.py`
  - `dashboard_schemas.py`
  - `context_schemas.py`
  - `system_schemas.py`

## Mapping of Key Models
- `ProcessedUnderlyingAggregatesV2_5` → `processed_data.py`
- `AISystemHealthV2_5` → `system_schemas.py`
- `ControlPanelParametersV2_5` → `configuration_schemas.py`
- `DynamicThresholdsV2_5` → `context_schemas.py`

## Migration Steps
1. Update all import statements from `data_models.eots_schemas_v2_5` to the appropriate new location
2. Verify model imports and usages
3. Remove deprecated references

## Notes
- Some models may have been slightly modified during the refactoring
- Always validate model structures after migration 