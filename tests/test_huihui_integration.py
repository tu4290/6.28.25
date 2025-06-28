#!/usr/bin/env python3
"""
HuiHui Integration Test Script
=============================

Tests HuiHui model integration and prepares for OpenAI replacement.
"""

import sys
import os
sys.path.append('.')

def test_huihui_experts():
    """Test all 4 HuiHui experts."""
    print("🧠 Testing HuiHui-MoE Expert System...")
    print("=" * 50)
    
    try:
        from huihui_integration.core.local_llm_client import LocalLLMClient
        
        client = LocalLLMClient()
        
        # Test connection
        if not client.test_connection():
            print("❌ Cannot connect to Ollama server")
            print("Please start Ollama: ollama serve")
            return False
        
        print("✅ Connected to Ollama server")
        
        # Test each expert
        experts = [
            ("market_regime", "Analyze current SPY market regime and volatility patterns"),
            ("options_flow", "Interpret VAPI-FA signal of +2.1 and DWFD of -1.5"),
            ("sentiment", "Analyze market sentiment from recent Fed policy news"),
            ("orchestrator", "Synthesize market analysis and provide strategic recommendation")
        ]
        
        for expert, prompt in experts:
            print(f"\n🎯 Testing {expert.replace('_', ' ').title()} Expert:")
            try:
                response = client.chat_huihui(prompt, expert)
                if "error" not in response.lower():
                    print(f"✅ {expert} expert working - Response length: {len(response)} chars")
                    print(f"Preview: {response[:100]}...")
                else:
                    print(f"❌ {expert} expert error: {response}")
                    return False
            except Exception as e:
                print(f"❌ {expert} expert failed: {e}")
                return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_ai_router():
    """Test AI router integration."""
    print("\n🤖 Testing AI Router Integration...")
    print("=" * 50)
    
    try:
        from huihui_integration.core.ai_model_router import AIRouter
        
        router = AIRouter()
        
        # Test automatic routing to HuiHui
        print("\n🎯 Testing Automatic EOTS Analysis Routing:")
        response = router.ask("Analyze SPY options flow and market regime")
        
        print(f"Model Used: {response['model_used']}")
        print(f"Task Type: {response['task_type']}")
        print(f"Response Time: {response['response_time']}s")
        print(f"Response Preview: {response['response'][:150]}...")
        
        # Verify it routed to HuiHui
        if "HuiHui" in response['model_used']:
            print("✅ Successfully routed EOTS analysis to HuiHui")
        else:
            print(f"❌ Did not route to HuiHui, used: {response['model_used']}")
            return False
        
        # Test direct EOTS method
        print("\n🧠 Testing Direct EOTS Analysis Method:")
        eots_response = router.eots_analysis("What is the current VIX regime?")
        print(f"Direct EOTS Response: {eots_response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Router test failed: {e}")
        return False

def scan_openai_usage():
    """Scan codebase for remaining OpenAI usage that needs replacement."""
    print("\n🔍 Scanning for Remaining OpenAI Usage...")
    print("=" * 50)

    openai_files = []
    openai_patterns = [
        "from openai import",
        "import openai",
        "openai.",
        "OpenAI(",
        "gpt-4",
        "gpt-3.5",
        "text-davinci",
        "OpenAIModel",
        "OPENAI_API_KEY"
    ]
    
    # Scan key directories
    scan_dirs = [
        "dashboard_application/modes/ai_dashboard",
        "core_analytics_engine", 
        "config",
        "utils"
    ]
    
    for scan_dir in scan_dirs:
        if os.path.exists(scan_dir):
            for root, dirs, files in os.walk(scan_dir):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                for pattern in openai_patterns:
                                    if pattern in content:
                                        openai_files.append((file_path, pattern))
                                        break
                        except Exception:
                            continue
    
    if openai_files:
        print(f"📋 Found {len(openai_files)} files with OpenAI usage:")
        for file_path, pattern in openai_files:
            print(f"  - {file_path} (contains: {pattern})")
    else:
        print("✅ No OpenAI usage found in scanned directories")
    
    return openai_files

def main():
    """Main test function."""
    print("🚀 HuiHui Integration & OpenAI Replacement Test")
    print("=" * 60)
    
    # Test HuiHui experts
    huihui_success = test_huihui_experts()
    
    # Test AI router
    router_success = test_ai_router()
    
    # Scan for OpenAI usage
    openai_files = scan_openai_usage()
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 30)
    print(f"HuiHui Experts: {'✅ PASS' if huihui_success else '❌ FAIL'}")
    print(f"AI Router: {'✅ PASS' if router_success else '❌ FAIL'}")
    print(f"OpenAI Files Found: {len(openai_files)} files need replacement")
    
    if huihui_success and router_success:
        print("\n🎉 HuiHui is ready for OpenAI replacement!")
        print("Next steps:")
        print("1. Replace OpenAI models in Pydantic AI agents")
        print("2. Update configuration files")
        print("3. Test all AI components")
    else:
        print("\n⚠️ Fix issues before proceeding with OpenAI replacement")

if __name__ == "__main__":
    main()
