#!/usr/bin/env python3
"""Test script to diagnose data pipeline issues"""

import sys
import os
import asyncio
import logging
import builtins

# Add project root to path
sys.path.insert(0, '.')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_data_pipeline():
    """Test the data pipeline step by step"""
    
    try:
        # Test 1: Environment variables
        print("🔍 Testing environment variables...")
        required_vars = ['CONVEX_EMAIL', 'CONVEX_PASSWORD', 'TRADIER_PRODUCTION_TOKEN']
        for var in required_vars:
            status = "✅" if var in os.environ else "❌"
            print(f"  {status} {var}: {'SET' if var in os.environ else 'MISSING'}")
        
        # Test 2: Config manager
        print("\n🔍 Testing config manager...")
        from utils.config_manager_v2_5 import ConfigManagerV2_5
        config_manager = ConfigManagerV2_5()
        print("  ✅ Config manager initialized")
        
        # Test 3: Database manager and global setup
        print("\n🔍 Testing database manager and global setup...")
        from data_management.database_manager_v2_5 import DatabaseManagerV2_5
        db_manager = DatabaseManagerV2_5()
        # Set global db_manager for historical data manager
        builtins.db_manager = db_manager
        print("  ✅ Database manager initialized and set as global")
        
        # Test 4: ConvexValue fetcher
        print("\n🔍 Testing ConvexValue fetcher...")
        from data_management.convexvalue_data_fetcher_v2_5 import ConvexValueDataFetcherV2_5
        fetcher = ConvexValueDataFetcherV2_5(config_manager)
        print("  ✅ ConvexValue fetcher initialized")
        
        # Test 5: Fetch raw data using correct method
        print("\n🔍 Testing raw data fetch for SPY...")
        try:
            chain_data, underlying_data = await fetcher.fetch_chain_and_underlying(
                session=None,
                symbol='SPY',
                dte_min=0,
                dte_max=45,
                price_range_percent=20
            )
            
            if underlying_data:
                print(f"  ✅ Underlying data fetched: {type(underlying_data)}")
                print(f"  📊 Price: {getattr(underlying_data, 'price', 'N/A')}")
            else:
                print("  ❌ No underlying data returned")
                
            if chain_data:
                print(f"  ✅ Options data fetched: {len(chain_data)} contracts")
                if len(chain_data) > 0:
                    sample_contract = chain_data[0]
                    print(f"  📊 Sample contract: {sample_contract.contract_symbol}")
            else:
                print("  ❌ No options data returned")
                
        except Exception as e:
            print(f"  ❌ Raw data fetch failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Test 6: Test metrics calculator and initial processor
        print("\n🔍 Testing metrics calculator and initial processor...")
        try:
            from data_management.historical_data_manager_v2_5 import HistoricalDataManagerV2_5
            from core_analytics_engine.metrics_calculator_v2_5 import MetricsCalculatorV2_5
            from data_management.initial_processor_v2_5 import InitialDataProcessorV2_5
            
            historical_manager = HistoricalDataManagerV2_5(config_manager)
            metrics_calc = MetricsCalculatorV2_5(config_manager, historical_manager)
            initial_processor = InitialDataProcessorV2_5(config_manager, metrics_calc)
            print("  ✅ Metrics calculator and initial processor initialized")
            
            # Test processing pipeline if we have data
            if underlying_data and chain_data:
                print("\n🔍 Testing complete data processing pipeline...")
                from data_models.raw_data import UnprocessedDataBundleV2_5
                from datetime import datetime
                
                # Create raw bundle
                raw_bundle = UnprocessedDataBundleV2_5(
                    options_contracts=chain_data,
                    underlying_data=underlying_data,
                    fetch_timestamp=datetime.now(),
                    errors=[]
                )
                print("  ✅ Raw data bundle created")
                
                # Process the data
                processed_bundle = initial_processor.process_data_and_calculate_metrics(
                    raw_data_bundle=raw_bundle,
                    dte_max=45
                )
                print("  ✅ Data processing completed!")
                print(f"  📊 Options with metrics: {len(processed_bundle.options_data_with_metrics)}")
                print(f"  🎯 Strike levels with metrics: {len(processed_bundle.strike_level_data_with_metrics)}")
                
        except Exception as e:
            print(f"  ❌ Metrics calculator/processor failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Test 7: Test orchestrator with fixed data pipeline
        print("\n🔍 Testing orchestrator with fixed data pipeline...")
        try:
            from core_analytics_engine.its_orchestrator_v2_5 import ITSOrchestratorV2_5
            orchestrator = ITSOrchestratorV2_5(config_manager, db_manager)
            print("  ✅ Orchestrator initialized")
            print(f"  📊 Status: {orchestrator.performance_metrics.get('system_status', 'UNKNOWN')}")
            
            # Test the fixed data pipeline
            print("\n🔍 Testing orchestrator data fetching...")
            processed_data = await orchestrator._get_processed_data_bundle('SPY')
            if processed_data:
                print("  ✅ Orchestrator data pipeline working!")
                print(f"  📊 Options with metrics: {len(processed_data.options_data_with_metrics)}")
                print(f"  🎯 Strike levels with metrics: {len(processed_data.strike_level_data_with_metrics)}")
            else:
                print("  ❌ Orchestrator data pipeline failed")
                
        except Exception as e:
            print(f"  ❌ Orchestrator failed: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n🎯 Data pipeline test completed!")
        
    except Exception as e:
        print(f"\n❌ Critical error in data pipeline test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_data_pipeline()) 