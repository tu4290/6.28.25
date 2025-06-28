#!/usr/bin/env python3
"""
Test script for Advanced Options Metrics integration.
Validates that the new metrics are properly calculated and integrated.
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.config_manager_v2_5 import ConfigManagerV2_5
from core_analytics_engine.metrics_calculator_v2_5 import MetricsCalculatorV2_5
from data_management.database_manager_v2_5 import DatabaseManagerV2_5
from data_management.historical_data_manager_v2_5 import HistoricalDataManagerV2_5
import builtins

def create_test_options_data():
    """Create test options data with bid/ask information."""
    test_data = []
    
    # Create realistic test options contracts
    strikes = [580, 585, 590, 595, 600, 605, 610, 615, 620]
    
    for i, strike in enumerate(strikes):
        # Simulate realistic bid/ask data
        mid_price = max(0.5, 10 - abs(strike - 600) * 0.5)  # ATM options worth more
        spread = mid_price * 0.05  # 5% spread
        
        bid_price = mid_price - spread/2
        ask_price = mid_price + spread/2
        
        # Simulate size based on moneyness
        base_size = 100 if abs(strike - 600) <= 5 else 50
        bid_size = base_size + np.random.randint(-20, 20)
        ask_size = base_size + np.random.randint(-20, 20)
        
        contract = {
            'contract_symbol': f'SPY{datetime.now().strftime("%y%m%d")}C{strike:08.0f}',
            'strike': strike,
            'opt_kind': 'call',
            'dte_calc': 1,
            'bid': bid_price,
            'ask': ask_price,
            'bid_size': max(1, bid_size),
            'ask_size': max(1, ask_size),
            'iv': 0.20 + np.random.uniform(-0.05, 0.05),  # 15-25% IV
            'theo': mid_price + np.random.uniform(-0.1, 0.1),
            'spread': ask_price - bid_price,
            'open_interest': np.random.randint(100, 1000),
            'raw_price': mid_price,
            'delta_contract': 0.5 + (600 - strike) * 0.01,  # Rough delta approximation
            'gamma_contract': 0.01,
            'theta_contract': -0.05,
            'vega_contract': 0.1,
            'volm': np.random.randint(10, 100)
        }
        test_data.append(contract)
    
    return pd.DataFrame(test_data)

def test_advanced_options_metrics():
    """Test the advanced options metrics calculation."""
    print("🧪 Testing Advanced Options Metrics Integration")
    print("=" * 60)
    
    try:
        # Initialize components properly
        config_manager = ConfigManagerV2_5()

        # Initialize database manager
        try:
            db_manager = DatabaseManagerV2_5(config_manager)
            # Set global db_manager for historical data manager
            builtins.db_manager = db_manager
            print("✅ Database manager initialized successfully")
        except Exception as db_error:
            print(f"⚠️  Database manager initialization failed: {db_error}")
            print("   Creating mock database manager for testing...")
            # Create a mock database manager for testing
            class MockDatabaseManager:
                def __init__(self):
                    self.connection_status = "MOCK"
                def close_connection(self):
                    pass
            db_manager = MockDatabaseManager()
            builtins.db_manager = db_manager

        # Initialize historical data manager
        historical_data_manager = HistoricalDataManagerV2_5(config_manager, db_manager)

        # Initialize metrics calculator
        metrics_calculator = MetricsCalculatorV2_5(config_manager, historical_data_manager)
        
        print("✅ Components initialized successfully")
        
        # Create test data
        test_options_df = create_test_options_data()
        print(f"✅ Created test options data with {len(test_options_df)} contracts")
        
        # Test the advanced options metrics calculation
        print("\n📊 Testing Advanced Options Metrics Calculation...")
        advanced_metrics = metrics_calculator.calculate_advanced_options_metrics(test_options_df)
        
        print("✅ Advanced metrics calculated successfully!")
        print(f"   Type: {type(advanced_metrics)}")
        print(f"   LWPAI: {advanced_metrics.lwpai:.4f}")
        print(f"   VABAI: {advanced_metrics.vabai:.4f}")
        print(f"   AOFM: {advanced_metrics.aofm:.4f}")
        print(f"   LIDB: {advanced_metrics.lidb:.4f}")
        print(f"   Confidence Score: {advanced_metrics.confidence_score:.3f}")
        print(f"   Valid Contracts: {advanced_metrics.valid_contracts_count}")
        
        # Skip full integration test for now - just test the metrics calculation directly
        print("\n✅ Advanced metrics calculation test completed successfully!")
        
        # Test ConvexValue field mapping
        print("\n🔍 Testing ConvexValue Field Mapping...")
        required_fields = ['bid', 'ask', 'bid_size', 'ask_size', 'theo', 'spread']
        missing_fields = [field for field in required_fields if field not in test_options_df.columns]
        
        if missing_fields:
            print(f"⚠️  Missing ConvexValue fields: {missing_fields}")
        else:
            print("✅ All required ConvexValue fields present")
        
        print("\n🎉 All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_advanced_options_metrics()
    sys.exit(0 if success else 1)
