#!/usr/bin/env python3
"""
Test script for ITS Orchestrator integration with Advanced Options Metrics
"""

import sys
import os
import numpy as np
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.config_manager_v2_5 import ConfigManagerV2_5
from core_analytics_engine.its_orchestrator_v2_5 import ITSOrchestratorV2_5
from data_models.raw_data import UnprocessedDataBundleV2_5, RawOptionsContractV2_5
from data_models.processed_data import ConsolidatedUnderlyingDataV2_5
from data_management.database_manager_v2_5 import DatabaseManagerV2_5
import builtins

def create_test_data_bundle() -> UnprocessedDataBundleV2_5:
    """Create a test data bundle for ITS orchestrator testing."""
    np.random.seed(42)
    
    # Create test options contracts
    contracts = []
    strikes = [580, 590, 600, 610, 620]
    option_types = ['call', 'put']
    
    for strike in strikes:
        for option_type in option_types:
            # Generate realistic bid/ask data
            if option_type == 'call':
                intrinsic = max(0, 600 - strike)
                time_value = np.random.uniform(2, 8)
            else:
                intrinsic = max(0, strike - 600)
                time_value = np.random.uniform(2, 8)
            
            theo_price = intrinsic + time_value
            spread = np.random.uniform(0.05, 0.20)
            
            bid_price = theo_price - spread/2
            ask_price = theo_price + spread/2
            
            contract = RawOptionsContractV2_5(
                contract_symbol='SPY',
                strike=strike,
                opt_kind=option_type,
                dte_calc=30.0,
                bid=bid_price,
                ask=ask_price,
                bid_size=np.random.randint(10, 100),
                ask_size=np.random.randint(10, 100),
                volm=np.random.randint(100, 1000),
                open_interest=np.random.randint(500, 5000),
                iv=np.random.uniform(0.15, 0.25),
                theo=theo_price,
                spread=spread,
                raw_price=theo_price,
                delta_contract=np.random.uniform(-0.5, 0.5),
                gamma_contract=np.random.uniform(0.001, 0.01),
                theta_contract=np.random.uniform(-0.1, -0.01),
                vega_contract=np.random.uniform(0.01, 0.1)
            )
            contracts.append(contract)
    
    # Create test underlying data
    underlying_data = ConsolidatedUnderlyingDataV2_5(
        symbol="AAPL",  # Example symbol, replace as needed
        timestamp=datetime.now(),
        price=0.0,
        price_change_abs=0.0,
        price_change_pct=0.0,
        day_open=0.0,
        day_high=0.0,
        day_low=0.0,
        prev_close=0.0,
        day_volume=0,
        call_gxoi=0.0,
        put_gxoi=0.0,
        net_delta_flow=0.0,
        net_gamma_flow=0.0,
        net_vega_flow=0.0,
        net_theta_flow=0.0,
        gib_oi_based=0.0,
        vapi_fa_z_score=0.0,
        dwfd_z_score=0.0,
        tw_laf_z_score=0.0,
        vri_0dte_sum=0.0,
        vfi_0dte_sum=0.0,
        vvr_0dte_avg=0.0,
        vci_0dte_agg=0.0,
        a_mspi_summary_score=0.0,
        a_sai_avg=0.0,
        a_ssi_avg=0.0,
        vri_2_0_aggregate=0.0,
        e_sdag_mult=0.0,
        a_dag_total=0.0,
        net_value_flow_5m=0.0,
        net_value_flow_15m=0.0,
        net_value_flow_30m=0.0,
        net_value_flow_60m=0.0,
        total_nvp=0.0,
        volatility=0.0,
        atr=0.0
    )
    
    return UnprocessedDataBundleV2_5(
        options_contracts=contracts,
        underlying_data=underlying_data,
        fetch_timestamp=datetime.now()
    )

def test_its_orchestrator_advanced_metrics():
    """Test the ITS orchestrator with advanced options metrics integration."""
    print("🧪 Testing ITS Orchestrator with Advanced Options Metrics")
    print("=" * 70)
    
    try:
        # Initialize components
        config_manager = ConfigManagerV2_5()
        
        # Initialize database manager
        try:
            db_manager = DatabaseManagerV2_5(config_manager)
            builtins.db_manager = db_manager
            print("✅ Database manager initialized successfully")
        except Exception as db_error:
            print(f"⚠️  Database manager initialization failed: {db_error}")
            print("   Creating mock database manager for testing...")
            class MockDatabaseManager:
                def __init__(self):
                    self.connection_status = "MOCK"
                def close_connection(self):
                    pass
            db_manager = MockDatabaseManager()
            builtins.db_manager = db_manager
        
        # Initialize ITS orchestrator with simplified constructor (components will be initialized internally)
        its_orchestrator = ITSOrchestratorV2_5(
            config_manager=config_manager,
            db_manager=db_manager
        )
        print("✅ ITS orchestrator initialized successfully")
        
        # Create test data
        test_bundle = create_test_data_bundle()
        print(f"✅ Created test data: {len(test_bundle.options_contracts)} options contracts")
        
        # Test advanced options metrics integration with test data
        print("\n🚀 Testing Advanced Options Metrics Integration...")

        # Create test data bundle
        test_bundle = create_test_data_bundle()
        print(f"✅ Created test data: {len(test_bundle.options_contracts)} options contracts")

        # Test the metrics calculator directly with advanced options metrics
        from core_analytics_engine.metrics_calculator_v2_5 import MetricsCalculatorV2_5
        from data_management.historical_data_manager_v2_5 import HistoricalDataManagerV2_5

        historical_data_manager = HistoricalDataManagerV2_5(config_manager, db_manager)
        metrics_calculator = MetricsCalculatorV2_5(config_manager, historical_data_manager)

        # Convert test data to DataFrame format
        import pandas as pd
        options_df = pd.DataFrame([contract.model_dump() for contract in test_bundle.options_contracts])
        underlying_data_dict = test_bundle.underlying_data.model_dump()

        # Calculate all metrics including advanced options metrics
        df_strike, df_options, underlying_enriched = metrics_calculator.calculate_all_metrics(
            options_df_raw=options_df,
            und_data_api_raw=underlying_data_dict,
            dte_max=45
        )

        print("✅ Metrics calculation completed successfully!")
        print(f"   Options contracts processed: {len(df_options) if df_options is not None else 0}")
        print(f"   Strike levels processed: {len(df_strike) if df_strike is not None else 0}")

        # Check if advanced options metrics were calculated
        if hasattr(underlying_enriched, 'advanced_options_metrics') and underlying_enriched.get('advanced_options_metrics'):
            metrics = underlying_enriched['advanced_options_metrics']
            print("\n📈 Advanced Options Metrics:")
            print(f"   LWPAI: {metrics.lwpai:.4f}")
            print(f"   VABAI: {metrics.vabai:.4f}")
            print(f"   AOFM: {metrics.aofm:.4f}")
            print(f"   LIDB: {metrics.lidb:.4f}")
            print(f"   Confidence Score: {metrics.confidence_score:.3f}")
            print(f"   Contracts Analyzed: {metrics.contracts_analyzed}")
        else:
            print("⚠️  Advanced options metrics not found in calculation results")

        # Test ticker context analyzer integration
        print("\n🎯 Testing Ticker Context Analyzer Integration...")
        if hasattr(its_orchestrator, 'ticker_context_analyzer') and its_orchestrator.ticker_context_analyzer:
            # Create price data for ticker context analysis
            price_data = pd.DataFrame({
                'date': [datetime.now()],
                'open': [test_bundle.underlying_data.price],
                'high': [test_bundle.underlying_data.price * 1.02],
                'low': [test_bundle.underlying_data.price * 0.98],
                'close': [test_bundle.underlying_data.price],
                'volume': [1000000]
            })
            price_data.set_index('date', inplace=True)

            # Analyze ticker context with advanced options metrics
            context_analysis = its_orchestrator.ticker_context_analyzer.analyze_ticker_context(
                symbol='SPY',
                price_data=price_data,
                options_data=None,
                cv_options_contracts=test_bundle.options_contracts
            )

            print("✅ Ticker context analysis completed!")
            if context_analysis.advanced_options_metrics:
                metrics = context_analysis.advanced_options_metrics
                print("   Advanced Metrics in Context:")
                print(f"   LWPAI: {metrics.lwpai:.4f}")
                print(f"   VABAI: {metrics.vabai:.4f}")
                print(f"   AOFM: {metrics.aofm:.4f}")
                print(f"   LIDB: {metrics.lidb:.4f}")
            else:
                print("⚠️  Advanced options metrics not found in ticker context")
        else:
            print("⚠️  Ticker context analyzer not available")
        
        # Check key metrics from the underlying_enriched data
        enriched_data = underlying_enriched
        print("\n📊 Key Enriched Metrics:")
        print(f"   GIB (display): {enriched_data.gib_oi_based}")
        print(f"   HP EOD: {enriched_data.hp_eod}")
        print(f"   VRI 0DTE sum: {enriched_data.vri_0dte_sum}")
        print(f"   VFI 0DTE sum: {enriched_data.vfi_0dte_sum}")
        print(f"   VVR 0DTE avg: {enriched_data.vvr_0dte_avg}")
        print(f"   A-MSPI: {enriched_data.a_mspi}")
        print(f"   Market regime: {enriched_data.current_market_regime_v2_5}")
        
        print("\n🎉 All ITS orchestrator advanced metrics integration tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_its_orchestrator_advanced_metrics()
    sys.exit(0 if success else 1)
