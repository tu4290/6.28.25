#!/usr/bin/env python3
"""
Test HuiHui Routing
===================

Debug script to see which models are being selected for different prompts.
"""

import sys
sys.path.append('.')

from huihui_integration.core.ai_model_router import AIRouter, TaskType

def test_routing():
    print("🔍 Testing AI Model Routing...")
    print("=" * 50)
    
    router = AIRouter()
    
    # Test prompts
    test_prompts = [
        "Hello, how are you?",
        "What's the market regime for SPY?",
        "Analyze options flow",
        "Show me VIX analysis",
        "Help me with Python code",
        "Calculate portfolio risk",
        "Research market trends",
        "What's the best trading strategy?",
        "Run SQL query",
        "EOTS analysis please",
        "Market sentiment today"
    ]
    
    for prompt in test_prompts:
        task_type = router.detect_task_type(prompt)
        model_info = router.models[task_type]
        
        print(f"📝 Prompt: '{prompt}'")
        print(f"🎯 Task Type: {task_type.value}")
        print(f"🤖 Model: {model_info['display_name']}")
        print(f"📋 Model Name: {model_info['name']}")
        print("-" * 50)

def test_direct_huihui():
    print("\n🎯 Testing Direct HuiHui Connection...")
    print("=" * 50)
    
    router = AIRouter()
    
    # Force EOTS analysis
    try:
        result = router.ask("Test connection", TaskType.EOTS_ANALYSIS)
        print(f"✅ HuiHui Response: {result['response'][:100]}...")
        print(f"⏱️ Response Time: {result['response_time']}s")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_routing()
    test_direct_huihui() 