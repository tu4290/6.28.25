The `metrics_calculator_v2_5.py` file, once a monolithic component, has undergone a comprehensive refactoring process. Its functionalities have been modularized and distributed across several specialized modules within the `core_analytics_engine/eots_metrics` directory, as well as other relevant core analytics components. This restructuring enhances maintainability, readability, and scalability by adhering to the principle of separation of concerns.

Below is a detailed breakdown of where each formula and metric from the original `metrics_calculator_v2_5.py` now resides within the new refactored structure:

### New Modular Structure Overview

The `eots_metrics` directory now contains several specialized calculator classes, each responsible for a specific tier or category of metrics:

*   **`base_calculator.py`**: Contains common utility methods, data conversion, caching mechanisms, and validation helpers used by all other calculators.
*   **`foundational_metrics.py`**: Focuses on core, Tier 1 metrics.
*   **`enhanced_flow_metrics.py`**: Handles Tier 3 Enhanced Rolling Flow Metrics.
*   **`adaptive_metrics.py`**: Manages Tier 2 Adaptive Metrics, including 0DTE suite components.
*   **`heatmap_metrics.py`**: Responsible for generating data for enhanced heatmap visualizations.
*   **`miscellaneous_metrics.py`**: Contains general-purpose metrics like ATR and advanced options metrics.
*   **`underlying_aggregates.py`**: Aggregates strike-level data into underlying-level metrics and handles certain data preparation for other engines.

Additionally, some higher-level analytical functions have been moved to their respective engine modules:

*   **`market_regime_engine_v2_5.py`**: Contains logic for market regime classification and related analyses.
*   **`ai_predictions_manager_v2_5.py`**: Manages AI-driven prediction signal strength.

### Detailed Formula Mapping

#### 1. Base Utilities (`core_analytics_engine/eots_metrics/base_calculator.py`)

This module serves as the foundation, providing shared functionalities:

*   **Data Conversion & Serialization**:
    *   `_convert_numpy_value`: Converts NumPy types to Python types.
    *   `_convert_dataframe_to_pydantic_models`: Generalizes DataFrame conversion to Pydantic models.
    *   `_serialize_dataframe_for_redis`: Serializes DataFrames for Redis.
    *   `_serialize_underlying_data_for_redis`: Serializes underlying data for Redis.
*   **Caching Helpers**:
    *   `_get_isolated_cache`: Retrieves isolated cache for a metric.
    *   `_store_metric_data`: Stores metric data in cache.
    *   `_get_metric_data`: Retrieves metric data from cache.
    *   `_add_to_intraday_cache`: Adds values to intraday cache (now integrated with `EnhancedCacheManagerV2_5`).
    *   `_seed_new_ticker_cache`: Seeds new ticker cache with baseline values.
    *   `_calculate_percentile_gauge_value`: Calculates percentile-based gauge values.
    *   `_normalize_flow`: Normalizes flow series using Z-score.
    *   `_load_intraday_cache`: Loads intraday cache using `EnhancedCacheManagerV2_5`.
    *   `_save_intraday_cache`: Saves intraday cache using `EnhancedCacheManagerV2_5`.
*   **Validation & Configuration**:
    *   `_validate_metric_bounds`: Validates metric values against bounds.
    *   `_validate_aggregates`: Validates and sanitizes aggregate metrics.
    *   `_perform_final_validation`: Performs final validation on calculated metrics.
    *   `_get_metric_config`: Retrieves configuration values for metric groups.
*   **Symbol Handling**:
    *   `sanitize_symbol`: Sanitizes ticker symbols.
    *   `_is_futures_symbol`: Determines if a symbol is a futures contract.
*   **DTE Scaling**:
    *   `_get_dte_scaling_factor`: Provides DTE scaling factors.

#### 2. Foundational Metrics (`core_analytics_engine/eots_metrics/foundational_metrics.py`)

This module calculates the core, Tier 1 metrics:

*   **Net Customer Greek Flows**:
    *   `_calculate_net_customer_greek_flows`: Calculates `net_cust_delta_flow_und`, `net_cust_gamma_flow_und`, `net_cust_vega_flow_und`, `net_cust_theta_flow_und`.
*   **Gamma Imbalance (GIB) & Related**:
    *   `_calculate_gib_based_metrics`: Calculates `gib_oi_based_und`, `gib_raw_gamma_units_und`, `gib_dollar_value_full_und`.
    *   `_calculate_hp_eod_und_v2_5`: Calculates End-of-Day Hedging Pressure (`hp_eod_und`).
    *   `_calculate_gib_based_metrics`: Also calculates Traded Dealer Gamma Imbalance (`td_gib_und`).

#### 3. Enhanced Flow Metrics (`core_analytics_engine/eots_metrics/enhanced_flow_metrics.py`)

This module is dedicated to the Tier 3 Enhanced Rolling Flow Metrics:

*   **Volatility-Adjusted Premium Intensity with Flow Acceleration (VAPI-FA)**:
    *   `_calculate_vapi_fa`: Calculates `vapi_fa_raw_und`, `vapi_fa_z_score_und`, `vapi_fa_pvr_5m_und`, `vapi_fa_flow_accel_5m_und`.
*   **Delta-Weighted Flow Divergence (DWFD)**:
    *   `_calculate_dwfd`: Calculates `dwfd_raw_und`, `dwfd_z_score_und`, `dwfd_fvd_und`.
*   **Time-Weighted Liquidity-Adjusted Flow (TW-LAF)**:
    *   `_calculate_tw_laf`: Calculates `tw_laf_raw_und`, `tw_laf_z_score_und`, `tw_laf_liquidity_factor_5m_und`, `tw_laf_time_weighted_sum_und`.

#### 4. Adaptive Metrics (`core_analytics_engine/eots_metrics/adaptive_metrics.py`)

This module handles the context-aware, Tier 2 Adaptive Metrics:

*   **Adaptive Delta Adjusted Gamma Exposure (A-DAG)**:
    *   `_calculate_a_dag`: Calculates `a_dag_exposure`, `a_dag_adaptive_alpha`, `a_dag_flow_alignment`, `a_dag_directional_multiplier`, `a_dag_strike`.
*   **Enhanced Skew and Delta Adjusted Gamma Exposure (E-SDAGs)**:
    *   `_calculate_e_sdag`: Calculates `e_sdag_mult_strike`, `e_sdag_dir_strike`, `e_sdag_w_strike`, `e_sdag_vf_strike`, and their adaptive weights.
    *   `_calculate_sgexoi_v2_5`: Calculates Enhanced Skew-Adjusted Gamma Exposure (`sgexoi_v2_5`).
*   **Dynamic Time Decay Pressure Indicator (D-TDPI) & Derivatives**:
    *   `_calculate_d_tdpi`: Calculates `d_tdpi_strike`, `e_ctr_strike` (Enhanced Charm Decay Rate), and `e_tdfi_strike` (Enhanced Time Decay Flow Imbalance).
*   **Concentration Indices**:
    *   `_calculate_concentration_indices`: Calculates Gamma Concentration Index (`gci_strike`) and Delta Concentration Index (`dci_strike`).
*   **Volatility Regime Indicator Version 2.0 (VRI 2.0)**:
    *   `_calculate_vri_2_0`: Calculates `vri_2_0_strike`.
*   **0DTE Suite**:
    *   `_calculate_0dte_suite`: Calculates `vri_0dte`, `vfi_0dte`, `vvr_0dte`, `gci_0dte`, `dci_0dte`, and `vci_0dte` (Vanna Concentration Index for 0DTE).
*   **Context Helpers**:
    *   `_get_volatility_context`: Determines volatility context.
    *   `_get_market_direction_bias`: Determines market direction bias.
    *   `_get_average_dte_context`: Determines DTE context.

#### 5. Heatmap Metrics (`core_analytics_engine/eots_metrics/heatmap_metrics.py`)

This module prepares data for the enhanced heatmap visualizations:

*   **Super Gamma-Delta Hedging Pressure (SGDHP) Data**:
    *   `_calculate_sgdhp_scores`: Calculates `sgdhp_score_strike`.
*   **Integrated Volatility Surface Dynamics (IVSDH) Data**:
    *   `_calculate_ivsdh_scores`: Calculates `ivsdh_score_strike`.
*   **Ultimate Greek Confluence (UGCH) Data**:
    *   `_calculate_ugch_scores`: Calculates `ugch_score_strike`.

#### 6. Miscellaneous Metrics (`core_analytics_engine/eots_metrics/miscellaneous_metrics.py`)

This module contains other important, general-purpose metrics:

*   **Average True Range (ATR)**:
    *   `calculate_atr`: Calculates the ATR for the underlying.
*   **Advanced Options Metrics**:
    *   `calculate_advanced_options_metrics`: Calculates Liquidity-Weighted Price Action Indicator (LWPAI), Volatility-Adjusted Bid/Ask Imbalance (VABAI), Aggressive Order Flow Momentum (AOFM), and Liquidity-Implied Directional Bias (LIDB).
    *   `_get_default_advanced_metrics`: Provides default values for advanced options metrics.

#### 7. Underlying Aggregates (`core_analytics_engine/eots_metrics/underlying_aggregates.py`)

This module aggregates strike-level data and prepares certain inputs for other engines:

*   **Underlying Aggregation**:
    *   `calculate_all_underlying_aggregates`: Aggregates various strike-level metrics (e.g., `total_dxoi_und`, `total_gxoi_und`, `total_nvp_und`, 0DTE suite aggregates, A-MSPI summary, VRI 2.0 aggregate, E-SDAG aggregate, A-DAG aggregate) to the underlying level.
*   **Rolling Flows Aggregation**:
    *   `_aggregate_rolling_flows_from_contracts`: Aggregates `net_value_flow_Xm_und` and `net_vol_flow_Xm_und` from contract-level data.
*   **Enhanced Flow Inputs Aggregation**:
    *   `_aggregate_enhanced_flow_inputs`: Aggregates `total_nvp` and `total_nvp_vol` for DWFD and TW-LAF.
*   **Missing Regime Metrics**:
    *   `_add_missing_regime_metrics`: Adds fallback values for metrics required by the market regime engine (e.g., `is_SPX_0DTE_Friday_EOD`, `u_volatility`, `trend_threshold`, dynamic thresholds, `price_change_pct`).
*   **Intraday Rolling Flow Time Series**:
    *   `_build_rolling_flows_time_series`: Builds historical time series for rolling flows.
    *   `_prepare_current_rolling_flows_for_collector`: Prepares current rolling flows for the intraday collector.
    *   `_attach_historical_rolling_flows_from_collector`: Attaches historical rolling flows from the collector cache.

#### 8. Market Regime Analysis (`core_analytics_engine/market_regime_engine_v2_5.py`)

This module is responsible for classifying the market regime:

*   **Regime Classification**:
    *   `calculate_volatility_regime`: Calculates volatility regime score.
    *   `calculate_flow_intensity`: Calculates flow intensity score.
    *   `calculate_regime_stability`: Calculates regime stability score.
    *   `calculate_transition_momentum`: Calculates transition momentum score.
    *   `calculate_vri3_composite`: Calculates VRI 3.0 composite score.
    *   `calculate_confidence_level`: Calculates confidence level for the analysis.
    *   `calculate_regime_transition_probabilities`: Calculates transition probabilities to other regimes.
    *   `calculate_transition_timeframe`: Calculates expected transition timeframe.
    *   `analyze_equity_regime`, `analyze_bond_regime`, `analyze_commodity_regime`, `analyze_currency_regime`: Analyze specific market regimes.
    *   `generate_regime_description`: Generates detailed regime descriptions.
    *   `classify_regime`: Classifies the current market regime.

#### 9. AI Prediction Signal Strength (`core_analytics_engine/ai_predictions_manager_v2_5.py`)

This module now includes the AI prediction signal strength calculation:

*   **AI Prediction Signal Strength**:
    *   `calculate_ai_prediction_signal_strength`: Calculates composite signal strength, confidence score, and prediction direction based on various Z-score metrics (VAPI-FA, DWFD, TW-LAF).