"""
Vectorized AI Router Performance Test - "SPEED DEMON UNLEASHED" 🚀
================================================================

This test demonstrates the massive performance improvements of the vectorized AI router:
- Async/await vs synchronous processing
- Connection pooling vs new connections
- Vectorized batch processing vs sequential
- Pre-compiled patterns vs runtime compilation

Expected Results:
- Old Router: 30+ seconds per query (sequential)
- New Router: 5-10 seconds per query (async)
- Batch Processing: 4 queries in ~15 seconds vs ~120 seconds

Author: EOTS v2.5 Performance Engineering Team
"""

import asyncio
import time
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from huihui_integration.core.ai_model_router import AIRouter  # Old router
from huihui_integration.core.vectorized_ai_router import VectorizedAIRouter  # New router

async def test_old_router_performance():
    """🐌 Test the old synchronous AI router performance."""
    print("🐌 Testing OLD AI ROUTER (Synchronous)...")
    print("=" * 50)
    
    router = AIRouter()
    
    test_prompts = [
        "What's the current market regime for SPY?",
        "Analyze the options flow patterns in QQQ", 
        "What's the market sentiment right now?",
        "Give me a strategic recommendation"
    ]
    
    total_start = time.time()
    results = []
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🔍 Query {i}/4: {prompt[:30]}...")
        start_time = time.time()
        
        try:
            result = router.ask(prompt)
            end_time = time.time()
            query_time = round(end_time - start_time, 2)
            
            print(f"  ⏱️ Time: {query_time}s")
            print(f"  🧠 Expert: {result.get('expert_used', 'Unknown')}")
            print(f"  📝 Response: {result.get('response', 'No response')[:100]}...")
            
            results.append({
                "prompt": prompt,
                "time": query_time,
                "expert": result.get('expert_used', 'Unknown'),
                "success": True
            })
            
        except Exception as e:
            end_time = time.time()
            query_time = round(end_time - start_time, 2)
            print(f"  ❌ Error: {str(e)}")
            results.append({
                "prompt": prompt,
                "time": query_time,
                "expert": "Error",
                "success": False
            })
    
    total_end = time.time()
    total_time = round(total_end - total_start, 2)
    
    print("\n🐌 OLD ROUTER RESULTS:")
    print(f"  📊 Total Time: {total_time}s")
    print(f"  📈 Average per Query: {total_time/len(test_prompts):.2f}s")
    print(f"  ✅ Success Rate: {sum(1 for r in results if r['success'])}/{len(results)}")
    
    return {
        "total_time": total_time,
        "avg_time": total_time/len(test_prompts),
        "results": results,
        "success_rate": sum(1 for r in results if r['success']) / len(results)
    }

async def test_new_router_performance():
    """⚡ Test the new vectorized AI router performance."""
    print("\n\n⚡ Testing NEW VECTORIZED AI ROUTER (Async)...")
    print("=" * 50)
    
    test_prompts = [
        "What's the current market regime for SPY?",
        "Analyze the options flow patterns in QQQ",
        "What's the market sentiment right now?", 
        "Give me a strategic recommendation"
    ]
    
    async with VectorizedAIRouter() as router:
        # Test individual queries
        print("\n🔥 Testing Individual Async Queries...")
        individual_start = time.time()
        individual_results = []
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n🔍 Query {i}/4: {prompt[:30]}...")
            start_time = time.time()
            
            try:
                result = await router.ask_async(prompt)
                end_time = time.time()
                query_time = round(end_time - start_time, 2)
                
                print(f"  ⏱️ Time: {query_time}s {result.get('speed_emoji', '⚡')}")
                print(f"  🧠 Expert: {result.get('expert_used', 'Unknown')}")
                print(f"  📝 Response: {result.get('response', 'No response')[:100]}...")
                
                individual_results.append({
                    "prompt": prompt,
                    "time": query_time,
                    "expert": result.get('expert_used', 'Unknown'),
                    "success": True
                })
                
            except Exception as e:
                end_time = time.time()
                query_time = round(end_time - start_time, 2)
                print(f"  ❌ Error: {str(e)}")
                individual_results.append({
                    "prompt": prompt,
                    "time": query_time,
                    "expert": "Error",
                    "success": False
                })
        
        individual_end = time.time()
        individual_total = round(individual_end - individual_start, 2)
        
        print("\n⚡ INDIVIDUAL ASYNC RESULTS:")
        print(f"  📊 Total Time: {individual_total}s")
        print(f"  📈 Average per Query: {individual_total/len(test_prompts):.2f}s")
        print(f"  ✅ Success Rate: {sum(1 for r in individual_results if r['success'])}/{len(individual_results)}")
        
        # Test vectorized batch processing
        print("\n\n🧠 Testing VECTORIZED BATCH PROCESSING...")
        print("🚀 Processing all 4 queries IN PARALLEL...")
        
        batch_start = time.time()
        try:
            batch_results = await router.ask_batch(test_prompts)
            batch_end = time.time()
            batch_total = round(batch_end - batch_start, 2)
            
            print("\n🚀 VECTORIZED BATCH RESULTS:")
            print(f"  📊 Total Time: {batch_total}s (ALL 4 QUERIES IN PARALLEL!)")
            print(f"  📈 Effective per Query: {batch_total/len(test_prompts):.2f}s")
            print(f"  ✅ Success Rate: {sum(1 for r in batch_results if 'Error' not in r.get('response', ''))}/{len(batch_results)}")
            
            for i, result in enumerate(batch_results, 1):
                print(f"  🔍 Query {i}: {result.get('response_time', 0):.2f}s {result.get('speed_emoji', '⚡')} - {result.get('expert_used', 'Unknown')}")
            
        except Exception as e:
            batch_end = time.time()
            batch_total = round(batch_end - batch_start, 2)
            print(f"  ❌ Batch Error: {str(e)}")
            batch_results = []
        
        # Performance stats
        stats = router.get_performance_stats()
        print("\n📊 PERFORMANCE STATISTICS:")
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")
    
    return {
        "individual_total": individual_total,
        "individual_avg": individual_total/len(test_prompts),
        "individual_results": individual_results,
        "batch_total": batch_total if 'batch_total' in locals() else 0,
        "batch_results": batch_results if 'batch_results' in locals() else [],
        "success_rate": sum(1 for r in individual_results if r['success']) / len(individual_results)
    }

async def performance_comparison():
    """🏁 Compare old vs new router performance."""
    print("🏁 PERFORMANCE COMPARISON: Old vs New AI Router")
    print("=" * 60)
    
    # Test old router
    old_results = await test_old_router_performance()
    
    # Test new router
    new_results = await test_new_router_performance()
    
    # Performance comparison
    print("\n\n🏆 FINAL PERFORMANCE COMPARISON")
    print("=" * 60)
    
    # Individual query comparison
    if old_results["avg_time"] > 0 and new_results["individual_avg"] > 0:
        individual_speedup = old_results["avg_time"] / new_results["individual_avg"]
        print("📈 INDIVIDUAL QUERY SPEEDUP:")
        print(f"  🐌 Old Router: {old_results['avg_time']:.2f}s per query")
        print(f"  ⚡ New Router: {new_results['individual_avg']:.2f}s per query")
        print(f"  🚀 SPEEDUP: {individual_speedup:.2f}x FASTER!")
    
    # Batch processing comparison
    if old_results["total_time"] > 0 and new_results["batch_total"] > 0:
        batch_speedup = old_results["total_time"] / new_results["batch_total"]
        print("\n📈 BATCH PROCESSING SPEEDUP:")
        print(f"  🐌 Old Router (Sequential): {old_results['total_time']:.2f}s for 4 queries")
        print(f"  🧠 New Router (Vectorized): {new_results['batch_total']:.2f}s for 4 queries")
        print(f"  🚀 SPEEDUP: {batch_speedup:.2f}x FASTER!")
    
    # Success rate comparison
    print("\n📊 RELIABILITY COMPARISON:")
    print(f"  🐌 Old Router Success Rate: {old_results['success_rate']*100:.1f}%")
    print(f"  ⚡ New Router Success Rate: {new_results['success_rate']*100:.1f}%")
    
    # Summary
    print("\n🎯 SUMMARY:")
    if new_results["individual_avg"] < old_results["avg_time"]:
        print("  ✅ Vectorized router is significantly faster!")
        print("  ✅ Async processing eliminates blocking overhead!")
        print("  ✅ Connection pooling reduces connection setup time!")
        if new_results["batch_total"] > 0:
            print("  ✅ Batch processing enables true parallelization!")
    else:
        print("  ⚠️ Performance results need investigation")
    
    return {
        "old_results": old_results,
        "new_results": new_results
    }

if __name__ == "__main__":
    print("🚀 VECTORIZED AI ROUTER PERFORMANCE TEST")
    print("=" * 60)
    print("Testing the speed improvements of the new vectorized AI router...")
    print("This may take a few minutes to complete all tests.\n")
    
    try:
        # Run the performance comparison
        results = asyncio.run(performance_comparison())
        
        print("\n✅ Performance test completed successfully!")
        print("🚀 The vectorized router should show significant improvements!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc() 