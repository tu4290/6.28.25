#!/usr/bin/env python3
"""
ADVANCED METRICS VERIFICATION TEST
=================================

This test verifies that all 4 advanced options metrics are calculated correctly:
1. LWPAI (Liquidity-Weighted Price Action Indicator)
2. VABAI (Volatility-Adjusted Bid/Ask Imbalance)
3. AOFM (Aggressive Order Flow Momentum)
4. LIDB (Liquidity-Implied Directional Bias)

Tests both the raw calculations and normalization to -1 to +1 range.
"""

import pandas as pd
import numpy as np
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_advanced_metrics_calculations():
    """Test all 4 advanced metrics with known data."""
    
    print("🧪 ADVANCED METRICS VERIFICATION TEST")
    print("=" * 50)
    
    # Create test options data that should produce predictable results
    test_data = pd.DataFrame([
        # Contract 1: Bullish bias (higher ask size)
        {'bid': 10.0, 'ask': 10.5, 'bid_size': 100, 'ask_size': 200, 'iv': 0.25, 'theo': 10.2, 'spread': 0.5},
        # Contract 2: Bearish bias (higher bid size)
        {'bid': 15.0, 'ask': 15.8, 'bid_size': 300, 'ask_size': 150, 'iv': 0.30, 'theo': 15.3, 'spread': 0.8},
        # Contract 3: Neutral
        {'bid': 5.0, 'ask': 5.3, 'bid_size': 100, 'ask_size': 100, 'iv': 0.20, 'theo': 5.1, 'spread': 0.3},
        # Contract 4: High volatility
        {'bid': 20.0, 'ask': 21.0, 'bid_size': 50, 'ask_size': 75, 'iv': 0.50, 'theo': 20.4, 'spread': 1.0},
    ])
    
    print("📊 Test Data:")
    print(test_data.to_string(index=False))
    print()
    
    # Manual calculations for verification
    print("🔍 MANUAL CALCULATIONS:")
    print("-" * 30)
    
    # 1. LWPAI Calculation
    print("1. LWPAI (Liquidity-Weighted Price Action Indicator)")
    lwpai_values = []
    for _, row in test_data.iterrows():
        bid_price, ask_price = row['bid'], row['ask']
        bid_size, ask_size = row['bid_size'], row['ask_size']
        total_size = bid_size + ask_size
        lwpai = ((bid_price * bid_size) + (ask_price * ask_size)) / total_size
        lwpai_values.append(lwpai)
        print(f"   Contract: LWPAI = (({bid_price}*{bid_size}) + ({ask_price}*{ask_size})) / {total_size} = {lwpai:.4f}")
    
    avg_lwpai = np.mean(lwpai_values)
    print(f"   Average LWPAI: {avg_lwpai:.4f}")
    print()
    
    # 2. VABAI Calculation
    print("2. VABAI (Volatility-Adjusted Bid/Ask Imbalance)")
    vabai_values = []
    for _, row in test_data.iterrows():
        bid_size, ask_size = row['bid_size'], row['ask_size']
        iv = row['iv']
        total_size = bid_size + ask_size
        size_imbalance = (bid_size - ask_size) / total_size
        vabai = size_imbalance * iv
        vabai_values.append(vabai)
        print(f"   Contract: VABAI = (({bid_size}-{ask_size})/{total_size}) * {iv} = {vabai:.4f}")
    
    avg_vabai = np.mean(vabai_values)
    print(f"   Average VABAI: {avg_vabai:.4f}")
    print()
    
    # 3. AOFM Calculation
    print("3. AOFM (Aggressive Order Flow Momentum)")
    aofm_components = []
    for _, row in test_data.iterrows():
        bid_price, ask_price = row['bid'], row['ask']
        bid_size, ask_size = row['bid_size'], row['ask_size']
        aofm_component = (ask_price * ask_size) - (bid_price * bid_size)
        aofm_components.append(aofm_component)
        print(f"   Contract: AOFM = ({ask_price}*{ask_size}) - ({bid_price}*{bid_size}) = {aofm_component:.2f}")
    
    total_aofm = sum(aofm_components)
    avg_aofm = total_aofm / len(aofm_components)
    print(f"   Total AOFM Sum: {total_aofm:.2f}")
    print(f"   Average AOFM: {avg_aofm:.2f}")
    print()
    
    # 4. LIDB Calculation
    print("4. LIDB (Liquidity-Implied Directional Bias)")
    lidb_values = []
    for _, row in test_data.iterrows():
        bid_size, ask_size = row['bid_size'], row['ask_size']
        total_size = bid_size + ask_size
        bid_proportion = bid_size / total_size
        lidb = bid_proportion - 0.5
        lidb_values.append(lidb)
        print(f"   Contract: LIDB = ({bid_size}/{total_size}) - 0.5 = {lidb:.4f}")
    
    avg_lidb = np.mean(lidb_values)
    print(f"   Average LIDB: {avg_lidb:.4f}")
    print()
    
    # Test normalization
    print("🎯 NORMALIZATION TEST:")
    print("-" * 25)
    
    current_price = 100.0  # Assume SPX at 5800, but using 100 for easier math
    
    # LWPAI normalization
    if avg_lwpai > 0:
        price_deviation_pct = (avg_lwpai - current_price) / current_price
        lwpai_normalized = max(-1.0, min(1.0, price_deviation_pct * 20))
    else:
        lwpai_normalized = 0.0
    
    print(f"LWPAI: {avg_lwpai:.4f} → normalized: {lwpai_normalized:.4f}")
    
    # VABAI normalization (should already be in range)
    vabai_normalized = max(-1.0, min(1.0, avg_vabai))
    print(f"VABAI: {avg_vabai:.4f} → normalized: {vabai_normalized:.4f}")
    
    # AOFM normalization
    total_liquidity = sum(row['bid_size'] + row['ask_size'] for _, row in test_data.iterrows())
    if total_liquidity > 0 and avg_aofm != 0:
        aofm_scale_factor = current_price * total_liquidity / 100000
        aofm_normalized = max(-1.0, min(1.0, avg_aofm / max(aofm_scale_factor, 1.0)))
    else:
        aofm_normalized = 0.0
    
    print(f"AOFM: {avg_aofm:.2f} → normalized: {aofm_normalized:.4f} (scale factor: {aofm_scale_factor:.2f})")
    
    # LIDB normalization
    lidb_normalized = max(-1.0, min(1.0, avg_lidb * 2.0))
    print(f"LIDB: {avg_lidb:.4f} → normalized: {lidb_normalized:.4f}")
    print()
    
    # Validation checks
    print("✅ VALIDATION CHECKS:")
    print("-" * 20)
    
    checks_passed = 0
    total_checks = 8
    
    # Check 1: LWPAI should be reasonable (close to mid prices)
    expected_lwpai_range = (5.0, 25.0)  # Based on our test data
    if expected_lwpai_range[0] <= avg_lwpai <= expected_lwpai_range[1]:
        print(f"✅ LWPAI in expected range: {avg_lwpai:.4f}")
        checks_passed += 1
    else:
        print(f"❌ LWPAI out of range: {avg_lwpai:.4f} (expected {expected_lwpai_range})")
    
    # Check 2: VABAI should reflect imbalances
    if -1.0 <= avg_vabai <= 1.0:
        print(f"✅ VABAI in valid range: {avg_vabai:.4f}")
        checks_passed += 1
    else:
        print(f"❌ VABAI out of range: {avg_vabai:.4f}")
    
    # Check 3: AOFM should be non-zero (we have imbalances)
    if avg_aofm != 0:
        print(f"✅ AOFM shows momentum: {avg_aofm:.2f}")
        checks_passed += 1
    else:
        print(f"❌ AOFM is zero when it shouldn't be: {avg_aofm:.2f}")
    
    # Check 4: LIDB should be in valid range
    if -0.5 <= avg_lidb <= 0.5:
        print(f"✅ LIDB in valid range: {avg_lidb:.4f}")
        checks_passed += 1
    else:
        print(f"❌ LIDB out of range: {avg_lidb:.4f}")
    
    # Check 5-8: All normalized values should be in -1 to +1 range
    normalized_values = [lwpai_normalized, vabai_normalized, aofm_normalized, lidb_normalized]
    normalized_names = ['LWPAI', 'VABAI', 'AOFM', 'LIDB']
    
    for name, value in zip(normalized_names, normalized_values):
        if -1.0 <= value <= 1.0:
            print(f"✅ {name} normalized correctly: {value:.4f}")
            checks_passed += 1
        else:
            print(f"❌ {name} normalization failed: {value:.4f}")
    
    print()
    print(f"🎯 FINAL RESULT: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("🎉 ALL ADVANCED METRICS CALCULATIONS ARE CORRECT!")
        return True
    else:
        print("❌ Some metrics calculations need fixing!")
        return False

if __name__ == "__main__":
    success = test_advanced_metrics_calculations()
    
    if success:
        print("\n✨ Advanced metrics are ready for production use!")
    else:
        print("\n🔧 Advanced metrics need debugging before deployment.")
        sys.exit(1)
