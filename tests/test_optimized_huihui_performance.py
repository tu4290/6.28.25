#!/usr/bin/env python3
"""
Test Optimized HuiHui Performance
Verify that our optimizations improved response times from 32+ seconds to ~12 seconds
"""

import time
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from huihui_integration.core.ai_model_router import AIRouter, HuiHuiExpertType

def test_optimized_performance():
    """Test the optimized HuiHui configuration."""
    
    print("🚀 Testing Optimized HuiHui Performance")
    print("=" * 50)
    print("Expected improvement: 32+ seconds → ~12 seconds")
    print()
    
    # Initialize the AI router with optimized settings
    router = AIRouter()
    
    # Test each expert type
    test_cases = [
        {
            "expert": HuiHuiExpertType.OPTIONS_FLOW,
            "prompt": "Analyze SPY options flow: VAPI-FA +1.5, DWFD -0.8, VRI 0.65. Quick analysis.",
            "description": "Options Flow Analysis"
        },
        {
            "expert": HuiHuiExpertType.MARKET_REGIME,
            "prompt": "Current VIX at 18.5, VRI_2_0 = 0.72. What's the market regime?",
            "description": "Market Regime Detection"
        },
        {
            "expert": HuiHuiExpertType.SENTIMENT,
            "prompt": "Fed hawkish tone, earnings season anxiety. Market sentiment analysis.",
            "description": "Sentiment Analysis"
        },
        {
            "expert": HuiHuiExpertType.ORCHESTRATOR,
            "prompt": "SPY analysis: VIX 18.5, Put/Call 1.2, VAPI-FA +1.5. Strategic recommendation.",
            "description": "Strategic Orchestration"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🧪 Test {i}/4: {test_case['description']}")
        print(f"   Expert: {test_case['expert'].value}")
        print(f"   Prompt: {test_case['prompt'][:60]}...")
        
        start_time = time.time()
        
        try:
            response = router.ask(test_case['prompt'], force_expert=test_case['expert'])
            end_time = time.time()
            
            response_time = round(end_time - start_time, 2)
            
            # Performance classification
            if response_time < 5:
                performance = "🚀 EXCELLENT"
                status = "✅"
            elif response_time < 10:
                performance = "⚡ GOOD"
                status = "✅"
            elif response_time < 15:
                performance = "⏱️ ACCEPTABLE"
                status = "✅"
            elif response_time < 25:
                performance = "🐌 SLOW"
                status = "⚠️"
            else:
                performance = "🐢 VERY SLOW"
                status = "❌"
            
            response_content = response.get('response', '')
            response_length = len(response_content)
            
            print(f"   {status} Time: {response_time}s - {performance}")
            print(f"   📝 Response: {response_length} chars")
            print(f"   🎯 Expert Used: {response.get('expert_used', 'Unknown')}")
            
            results.append({
                "test": test_case['description'],
                "expert": test_case['expert'].value,
                "success": True,
                "response_time": response_time,
                "performance": performance,
                "response_length": response_length
            })
            
        except Exception as e:
            end_time = time.time()
            response_time = round(end_time - start_time, 2)
            
            print(f"   ❌ Failed: {response_time}s - {str(e)}")
            
            results.append({
                "test": test_case['description'],
                "expert": test_case['expert'].value,
                "success": False,
                "response_time": response_time,
                "error": str(e)
            })
        
        print()
    
    # Performance summary
    print("📊 OPTIMIZATION RESULTS SUMMARY")
    print("=" * 50)
    
    successful_tests = [r for r in results if r["success"]]
    
    if successful_tests:
        avg_time = sum(r["response_time"] for r in successful_tests) / len(successful_tests)
        fastest_time = min(r["response_time"] for r in successful_tests)
        slowest_time = max(r["response_time"] for r in successful_tests)
        
        print(f"✅ Successful Tests: {len(successful_tests)}/{len(results)}")
        print(f"⚡ Average Response Time: {avg_time:.2f}s")
        print(f"🚀 Fastest Response: {fastest_time:.2f}s")
        print(f"🐌 Slowest Response: {slowest_time:.2f}s")
        
        # Compare to previous performance
        previous_time = 32.8  # From our earlier test
        improvement = previous_time - avg_time
        improvement_percent = (improvement / previous_time) * 100
        
        print("\n🎯 PERFORMANCE IMPROVEMENT:")
        print(f"   Before Optimization: {previous_time}s")
        print(f"   After Optimization: {avg_time:.2f}s")
        print(f"   Improvement: {improvement:.1f}s ({improvement_percent:.1f}% faster)")
        
        if avg_time < 15:
            print("   🎉 SUCCESS: Achieved target performance!")
        else:
            print("   ⚠️ Still slow, but improved")
            
    else:
        print("❌ No successful tests - optimization failed")
    
    return results

if __name__ == "__main__":
    test_optimized_performance() 