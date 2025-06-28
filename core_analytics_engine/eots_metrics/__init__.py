# core_analytics_engine/eots_metrics/__init__.py

"""
EOTS Metrics Module - Refactored from metrics_calculator_v2_5.py

This module contains the refactored metric calculation classes that were previously
in the monolithic metrics_calculator_v2_5.py file.
"""

from .base_calculator import BaseCalculator, MetricCalculationState, MetricCache, MetricCacheConfig
from .foundational_metrics import FoundationalMetricsCalculator
from .enhanced_flow_metrics import EnhancedFlowMetricsCalculator
from .adaptive_metrics import AdaptiveMetricsCalculator
from .heatmap_metrics import HeatmapMetricsCalculator
from .miscellaneous_metrics import MiscellaneousMetricsCalculator
from .underlying_aggregates import UnderlyingAggregatesCalculator
from .elite_impact_calculations import EliteImpactCalculator
from core_analytics_engine.eots_metrics.elite_definitions import EliteConfig
from data_models.processed_data import ProcessedDataBundleV2_5, ProcessedUnderlyingAggregatesV2_5

# For backward compatibility, create a composite calculator that combines all modules
class MetricsCalculatorV2_5:
    """
    Composite calculator that combines all the refactored metric calculators
    for backward compatibility with existing code.
    """
    
    def __init__(self, config_manager, historical_data_manager, enhanced_cache_manager, elite_config=None):
        # Ensure elite_config is a Pydantic model
        if elite_config is None:
            elite_config = EliteConfig()
        elif not isinstance(elite_config, EliteConfig):
            elite_config = EliteConfig.model_validate(elite_config)
        self.foundational = FoundationalMetricsCalculator(config_manager, historical_data_manager)  # Standalone class - 2 params
        self.heatmap = HeatmapMetricsCalculator(config_manager, historical_data_manager, enhanced_cache_manager)  # BaseCalculator - 3 params
        self.miscellaneous = MiscellaneousMetricsCalculator(config_manager, historical_data_manager, enhanced_cache_manager)  # BaseCalculator - 3 params
        self.elite_impact = EliteImpactCalculator(elite_config)  # Standalone class - 1 param
        
        # Initialize calculators that require elite_config only if it's provided
        if elite_config is not None:
            self.enhanced_flow = EnhancedFlowMetricsCalculator(config_manager, historical_data_manager, enhanced_cache_manager, elite_config)
            self.adaptive = AdaptiveMetricsCalculator(config_manager, historical_data_manager, enhanced_cache_manager, elite_config)
            self.underlying_aggregates = UnderlyingAggregatesCalculator(config_manager, historical_data_manager, enhanced_cache_manager, elite_config)
        else:
            self.enhanced_flow = None
            self.adaptive = None
            self.underlying_aggregates = None
        
        # Store references for common access
        self.config_manager = config_manager
        self.historical_data_manager = historical_data_manager
        self.enhanced_cache_manager = enhanced_cache_manager
        self.elite_config = elite_config
    
    def process_data_bundle(self, options_data, underlying_data):
        """
        Process options and underlying data to create a ProcessedDataBundleV2_5.
        This method maintains backward compatibility with the orchestrator interface.
        """
        from datetime import datetime
        
        # Create a data bundle dictionary for compatibility
        data_bundle = {
            'options_data': options_data,
            'underlying_data': underlying_data,
            'strike_level_data': None  # Will be generated from options_data
        }
        
        # For now, create a minimal ProcessedDataBundleV2_5 with empty/default values
        # This is a temporary implementation to resolve the AttributeError
        try:
            # Create minimal underlying data
            underlying_data_processed = ProcessedUnderlyingAggregatesV2_5(
                symbol=underlying_data.get('symbol', 'UNKNOWN'),
                timestamp=datetime.now(),
                price=float(underlying_data.get('price', 0.0)),
                price_change_abs_und=0.0,
                price_change_pct_und=0.0,
                day_open_price_und=0.0,
                day_high_price_und=0.0,
                day_low_price_und=0.0,
                prev_day_close_price_und=0.0,
                u_volatility=0.0,
                day_volume=0,
                call_gxoi=0.0,
                put_gxoi=0.0,
                gammas_call_buy=0.0,
                gammas_call_sell=0.0,
                gammas_put_buy=0.0,
                gammas_put_sell=0.0,
                deltas_call_buy=0.0,
                deltas_call_sell=0.0,
                deltas_put_buy=0.0,
                deltas_put_sell=0.0,
                vegas_call_buy=0.0,
                vegas_call_sell=0.0,
                vegas_put_buy=0.0,
                vegas_put_sell=0.0,
                thetas_call_buy=0.0,
                thetas_call_sell=0.0,
                thetas_put_buy=0.0,
                thetas_put_sell=0.0,
                call_vxoi=0.0,
                put_vxoi=0.0,
                value_bs=0.0,
                volm_bs=0.0,
                deltas_buy=0.0,
                deltas_sell=0.0,
                vegas_buy=0.0,
                vegas_sell=0.0,
                thetas_buy=0.0,
                thetas_sell=0.0,
                volm_call_buy=0.0,
                volm_put_buy=0.0,
                volm_call_sell=0.0,
                volm_put_sell=0.0,
                value_call_buy=0.0,
                value_put_buy=0.0,
                value_call_sell=0.0,
                value_put_sell=0.0,
                vflowratio=0.0,
                dxoi=0.0,
                gxoi=0.0,
                vxoi=0.0,
                txoi=0.0,
                call_dxoi=0.0,
                put_dxoi=0.0,
                tradier_iv5_approx_smv_avg=0.0,
                total_call_oi_und=0.0,
                total_put_oi_und=0.0,
                total_call_vol_und=0.0,
                total_put_vol_und=0.0,
                tradier_open=0.0,
                tradier_high=0.0,
                tradier_low=0.0,
                tradier_close=0.0,
                tradier_volume=0.0,
                tradier_vwap=0.0,
                gib_oi_based_und=None,
                td_gib_und=None,
                hp_eod_und=None,
                net_cust_delta_flow_und=None,
                net_cust_gamma_flow_und=None,
                net_cust_vega_flow_und=None,
                net_cust_theta_flow_und=None,
                net_value_flow_5m_und=None,
                net_vol_flow_5m_und=None,
                net_value_flow_15m_und=None,
                net_vol_flow_15m_und=None,
                net_value_flow_30m_und=None,
                net_vol_flow_30m_und=None,
                net_value_flow_60m_und=None,
                net_vol_flow_60m_und=None,
                vri_0dte_und_sum=None,
                vfi_0dte_und_sum=None,
                vvr_0dte_und_avg=None,
                vci_0dte_agg=None,
                arfi_overall_und_avg=None,
                a_mspi_und_summary_score=None,
                a_sai_und_avg=None,
                a_ssi_und_avg=None,
                vri_2_0_und_aggregate=None,
                vapi_fa_z_score_und=None,
                dwfd_z_score_und=None,
                tw_laf_z_score_und=None,
                ivsdh_surface_data=None,
                current_market_regime_v2_5=None,
                ticker_context_dict_v2_5=None,
                atr_und=None,
                hist_vol_20d=None,
                impl_vol_atm=None,
                trend_strength=None,
                trend_direction=None,
                dynamic_thresholds=None,
                elite_impact_score_und=None,
                institutional_flow_score_und=None,
                flow_momentum_index_und=None,
                market_regime_elite=None,
                flow_type_elite=None,
                volatility_regime_elite=None,
                confidence=0.5,
                transition_risk=0.5
            )
            
            # Create minimal processed bundle
            processed_bundle = ProcessedDataBundleV2_5(
                options_data_with_metrics=[],  # Empty list for now
                strike_level_data_with_metrics=[],  # Empty list for now
                underlying_data_enriched=underlying_data_processed,
                processing_timestamp=datetime.now(),
                errors=[]
            )
            
            return processed_bundle
            
        except Exception as e:
            # If there's any error, create a minimal bundle with error info
            minimal_underlying = ProcessedUnderlyingAggregatesV2_5(
                symbol='ERROR',
                timestamp=datetime.now(),
                price=0.0,
                price_change_abs_und=0.0,
                price_change_pct_und=0.0,
                day_open_price_und=0.0,
                day_high_price_und=0.0,
                day_low_price_und=0.0,
                prev_day_close_price_und=0.0,
                u_volatility=0.0,
                day_volume=0.0,
                call_gxoi=0.0,
                put_gxoi=0.0,
                gammas_call_buy=0.0,
                gammas_call_sell=0.0,
                gammas_put_buy=0.0,
                gammas_put_sell=0.0,
                deltas_call_buy=0.0,
                deltas_call_sell=0.0,
                deltas_put_buy=0.0,
                deltas_put_sell=0.0,
                vegas_call_buy=0.0,
                vegas_call_sell=0.0,
                vegas_put_buy=0.0,
                vegas_put_sell=0.0,
                thetas_call_buy=0.0,
                thetas_call_sell=0.0,
                thetas_put_buy=0.0,
                thetas_put_sell=0.0,
                call_vxoi=0.0,
                put_vxoi=0.0,
                value_bs=0.0,
                volm_bs=0.0,
                deltas_buy=0.0,
                deltas_sell=0.0,
                vegas_buy=0.0,
                vegas_sell=0.0,
                thetas_buy=0.0,
                thetas_sell=0.0,
                volm_call_buy=0.0,
                volm_put_buy=0.0,
                volm_call_sell=0.0,
                volm_put_sell=0.0,
                value_call_buy=0.0,
                value_put_buy=0.0,
                value_call_sell=0.0,
                value_put_sell=0.0,
                vflowratio=0.0,
                dxoi=0.0,
                gxoi=0.0,
                vxoi=0.0,
                txoi=0.0,
                call_dxoi=0.0,
                put_dxoi=0.0,
                tradier_iv5_approx_smv_avg=0.0,
                total_call_oi_und=0.0,
                total_put_oi_und=0.0,
                total_call_vol_und=0.0,
                total_put_vol_und=0.0,
                tradier_open=0.0,
                tradier_high=0.0,
                tradier_low=0.0,
                tradier_close=0.0,
                tradier_volume=0.0,
                tradier_vwap=0.0,
                gib_oi_based_und=None,
                td_gib_und=None,
                hp_eod_und=None,
                net_cust_delta_flow_und=None,
                net_cust_gamma_flow_und=None,
                net_cust_vega_flow_und=None,
                net_cust_theta_flow_und=None,
                net_value_flow_5m_und=None,
                net_vol_flow_5m_und=None,
                net_value_flow_15m_und=None,
                net_vol_flow_15m_und=None,
                net_value_flow_30m_und=None,
                net_vol_flow_30m_und=None,
                net_value_flow_60m_und=None,
                net_vol_flow_60m_und=None,
                vri_0dte_und_sum=None,
                vfi_0dte_und_sum=None,
                vvr_0dte_und_avg=None,
                vci_0dte_agg=None,
                arfi_overall_und_avg=None,
                a_mspi_und_summary_score=None,
                a_sai_und_avg=None,
                a_ssi_und_avg=None,
                vri_2_0_und_aggregate=None,
                vapi_fa_z_score_und=None,
                dwfd_z_score_und=None,
                tw_laf_z_score_und=None,
                ivsdh_surface_data=None,
                current_market_regime_v2_5=None,
                ticker_context_dict_v2_5=None,
                atr_und=None,
                hist_vol_20d=None,
                impl_vol_atm=None,
                trend_strength=None,
                trend_direction=None,
                dynamic_thresholds=None,
                elite_impact_score_und=None,
                institutional_flow_score_und=None,
                flow_momentum_index_und=None,
                market_regime_elite=None,
                flow_type_elite=None,
                volatility_regime_elite=None,
                confidence=0.5,
                transition_risk=0.5
            )
            
            return ProcessedDataBundleV2_5(
                options_data_with_metrics=[],
                strike_level_data_with_metrics=[],
                underlying_data_enriched=minimal_underlying,
                processing_timestamp=datetime.now(),
                errors=[f"Error in process_data_bundle: {str(e)}"]
            )
    
    def calculate_all_metrics(self, options_df_raw, und_data_api_raw, dte_max=45):
        """
        Main method to calculate all metrics. This method orchestrates the individual calculators.
        
        Args:
            options_df_raw: DataFrame with raw options data
            und_data_api_raw: Dictionary with underlying data
            dte_max: Maximum DTE for calculations
            
        Returns:
            Tuple of (strike_level_df, contract_level_df, enriched_underlying_data)
        """
        import pandas as pd
        from datetime import datetime
        
        try:
            # Initialize contract level data
            df_chain_all_metrics = options_df_raw.copy() if not options_df_raw.empty else pd.DataFrame()
            
            # Create enriched underlying data with basic structure
            enriched_underlying = {
                'symbol': und_data_api_raw.get('symbol', 'UNKNOWN'),
                'timestamp': datetime.now(),
                'price': float(und_data_api_raw.get('price', 0.0)),
                'price_change_abs_und': 0.0,
                'price_change_pct_und': 0.0,
                'day_open_price_und': 0.0,
                'day_high_price_und': 0.0,
                'day_low_price_und': 0.0,
                'prev_day_close_price_und': 0.0,
                'u_volatility': 0.0,
                'day_volume': 0,
                # Add other required fields with default values
                'call_gxoi': 0.0,
                'put_gxoi': 0.0,
                'gammas_call_buy': 0.0,
                'gammas_call_sell': 0.0,
                'gammas_put_buy': 0.0,
                'gammas_put_sell': 0.0,
                'deltas_call_buy': 0.0,
                'deltas_call_sell': 0.0,
                'deltas_put_buy': 0.0,
                'deltas_put_sell': 0.0,
                'vegas_call_buy': 0.0,
                'vegas_call_sell': 0.0,
                'vegas_put_buy': 0.0,
                'vegas_put_sell': 0.0,
                'thetas_call_buy': 0.0,
                'thetas_call_sell': 0.0,
                'thetas_put_buy': 0.0,
                'thetas_put_sell': 0.0,
                'call_vxoi': 0.0,
                'put_vxoi': 0.0,
                'value_bs': 0.0,
                'volm_bs': 0.0,
                'deltas_buy': 0.0,
                'deltas_sell': 0.0,
                'vegas_buy': 0.0,
                'vegas_sell': 0.0,
                'thetas_buy': 0.0,
                'thetas_sell': 0.0,
                'volm_call_buy': 0.0,
                'volm_put_buy': 0.0,
                'volm_call_sell': 0.0,
                'volm_put_sell': 0.0,
                'value_call_buy': 0.0,
                'value_put_buy': 0.0,
                'value_call_sell': 0.0,
                'value_put_sell': 0.0,
                'vflowratio': 0.0,
                'dxoi': 0.0,
                'gxoi': 0.0,
                'vxoi': 0.0,
                'txoi': 0.0,
                'call_dxoi': 0.0,
                'put_dxoi': 0.0,
                'tradier_iv5_approx_smv_avg': 0.0,
                'total_call_oi_und': 0.0,
                'total_put_oi_und': 0.0,
                'total_call_vol_und': 0.0,
                'total_put_vol_und': 0.0,
                'tradier_open': 0.0,
                'tradier_high': 0.0,
                'tradier_low': 0.0,
                'tradier_close': 0.0,
                'tradier_volume': 0.0,
                'tradier_vwap': 0.0,
                'gib_oi_based_und': None,
                'td_gib_und': None,
                'hp_eod_und': None,
                'net_cust_delta_flow_und': None,
                'net_cust_gamma_flow_und': None,
                'net_cust_vega_flow_und': None,
                'net_cust_theta_flow_und': None,
                'net_value_flow_5m_und': None,
                'net_vol_flow_5m_und': None,
                'net_value_flow_15m_und': None,
                'net_vol_flow_15m_und': None,
                'net_value_flow_30m_und': None,
                'net_vol_flow_30m_und': None,
                'net_value_flow_60m_und': None,
                'net_vol_flow_60m_und': None,
                'vri_0dte_und_sum': None,
                'vfi_0dte_und_sum': None,
                'vvr_0dte_und_avg': None,
                'vci_0dte_agg': None,
                'arfi_overall_und_avg': None,
                'a_mspi_und_summary_score': None,
                'a_sai_und_avg': None,
                'a_ssi_und_avg': None,
                'vri_2_0_und_aggregate': None,
                'vapi_fa_z_score_und': None,
                'dwfd_z_score_und': None,
                'tw_laf_z_score_und': None,
                'ivsdh_surface_data': None,
                'current_market_regime_v2_5': None,
                'ticker_context_dict_v2_5': None,
                'atr_und': None,
                'hist_vol_20d': None,
                'impl_vol_atm': None,
                'trend_strength': None,
                'trend_direction': None,
                'dynamic_thresholds': None,
                'elite_impact_score_und': None,
                'institutional_flow_score_und': None,
                'flow_momentum_index_und': None,
                'market_regime_elite': None,
                'flow_type_elite': None,
                'volatility_regime_elite': None
            }
            
            # Generate strike-level data from options data
            df_strike_all_metrics = pd.DataFrame()
            
            if not options_df_raw.empty:
                # Create strike-level aggregation from contract data
                # Group by strike and aggregate key metrics
                strike_groups = options_df_raw.groupby('strike')
                
                strike_data = []
                for strike, group in strike_groups:
                    strike_row = {
                        'strike': float(strike),
                        'symbol': und_data_api_raw.get('symbol', 'UNKNOWN'),
                        'timestamp': datetime.now(),
                        'underlying_price': float(und_data_api_raw.get('price', 0.0)),
                        # Basic aggregations
                        'total_volume': group['volume'].sum() if 'volume' in group.columns else 0,
                        'total_open_interest': group['open_interest'].sum() if 'open_interest' in group.columns else 0,
                        'call_volume': group[group['option_type'] == 'call']['volume'].sum() if 'volume' in group.columns else 0,
                        'put_volume': group[group['option_type'] == 'put']['volume'].sum() if 'volume' in group.columns else 0,
                        'call_oi': group[group['option_type'] == 'call']['open_interest'].sum() if 'open_interest' in group.columns else 0,
                        'put_oi': group[group['option_type'] == 'put']['open_interest'].sum() if 'open_interest' in group.columns else 0,
                        # Initialize metrics that will be calculated by other calculators
                        'a_dag_score': 0.0,
                        'e_sdag_score': 0.0,
                        'vri_2_0_score': 0.0,
                        'vfi_0dte_score': 0.0,
                        'vvr_0dte_score': 0.0,
                        'vci_0dte_score': 0.0,
                        'sgdhp_score': 0.0,
                        'ivsdh_score': 0.0,
                        'ugch_score': 0.0
                    }
                    strike_data.append(strike_row)
                
                if strike_data:
                    df_strike_all_metrics = pd.DataFrame(strike_data)
            
            # Try to calculate foundational metrics if calculator is available
            try:
                if hasattr(self, 'foundational_calculator'):
                    foundational_metrics = self.foundational_calculator.calculate_all_foundational_metrics(und_data_api_raw)
                    enriched_underlying.update(foundational_metrics)
            except Exception as e:
                print(f"Warning: Could not calculate foundational metrics: {e}")
            
            # Try to calculate enhanced flow metrics if calculator is available
            try:
                if hasattr(self, 'enhanced_flow_calculator'):
                    symbol = und_data_api_raw.get('symbol', 'UNKNOWN')
                    flow_metrics = self.enhanced_flow_calculator.calculate_all_enhanced_flow_metrics(und_data_api_raw, symbol)
                    enriched_underlying.update(flow_metrics)
            except Exception as e:
                print(f"Warning: Could not calculate enhanced flow metrics: {e}")
            
            # Try to calculate adaptive metrics (strike-level) if calculator is available
            try:
                if hasattr(self, 'adaptive_calculator') and not df_strike_all_metrics.empty:
                    df_strike_all_metrics = self.adaptive_calculator.calculate_all_adaptive_metrics(df_strike_all_metrics, enriched_underlying)
            except Exception as e:
                print(f"Warning: Could not calculate adaptive metrics: {e}")
            
            # Try to calculate heatmap metrics (strike-level) if calculator is available
            try:
                if hasattr(self, 'heatmap_calculator') and not df_strike_all_metrics.empty:
                    df_strike_all_metrics = self.heatmap_calculator.calculate_all_heatmap_data(df_strike_all_metrics, enriched_underlying)
            except Exception as e:
                print(f"Warning: Could not calculate heatmap metrics: {e}")
            
            return df_strike_all_metrics, df_chain_all_metrics, enriched_underlying
            
        except Exception as e:
            print(f"Error in calculate_all_metrics: {e}")
            # Return empty/minimal data structures to prevent crashes
            return pd.DataFrame(), pd.DataFrame(), enriched_underlying
    
    def orchestrate_all_metric_calculations_v2_5(self, *args, **kwargs):
        """
        Main orchestration method that delegates to the appropriate calculators.
        This method maintains backward compatibility with the original interface.
        """
        # Delegate to calculate_all_metrics for now
        return self.calculate_all_metrics(*args, **kwargs)

__all__ = [
    'BaseCalculator',
    'MetricCalculationState', 
    'MetricCache',
    'MetricCacheConfig',
    'FoundationalMetricsCalculator',
    'EnhancedFlowMetricsCalculator', 
    'AdaptiveMetricsCalculator',
    'HeatmapMetricsCalculator',
    'MiscellaneousMetricsCalculator',
    'UnderlyingAggregatesCalculator',
    'EliteImpactCalculator',
    'MetricsCalculatorV2_5'  # For backward compatibility
]
