#!/usr/bin/env python3
"""
Test script to validate HuiHui market context enhancement.
Tests that HuiHui responds properly even when markets are closed.
"""

import sys
sys.path.append('.')

from elite_huihui_chat_production import EliteHuiHuiChat, get_market_status

def test_market_context():
    """Test the market context enhancement."""
    print("🧪 Testing HuiHui Market Context Enhancement")
    print("=" * 50)
    
    # Get market status
    market_info = get_market_status()
    print(f"📊 Current Market Status: {market_info['status']} ({market_info['context']})")
    print(f"🕐 Time: {market_info['time']} on {market_info['date']}")
    print()
    
    # Initialize chat
    chat = EliteHuiHuiChat()
    
    # Test prompt enhancement
    test_prompt = "What's your analysis of SPY right now?"
    enhanced_prompt = chat.enhance_prompt_with_context(test_prompt)
    
    print("🔍 Original Prompt:")
    print(f"   {test_prompt}")
    print()
    print("🚀 Enhanced Prompt:")
    print(f"   {enhanced_prompt[:200]}...")
    print()
    
    # Test with a simple query
    print("🤖 Testing HuiHui Response...")
    try:
        result = chat.router.ask(enhanced_prompt)
        
        if isinstance(result, dict):
            response = result.get("response", str(result))
            expert_used = result.get("expert_type", "Unknown")
        else:
            response = str(result)
            expert_used = "Unknown"
        
        print(f"✅ Expert Used: {expert_used}")
        print(f"📝 Response Length: {len(response)} characters")
        print(f"🎯 Response Preview: {response[:300]}...")
        
        # Check if response contains "market is closed"
        if "market is closed" in response.lower():
            print("❌ Still getting 'market is closed' response")
        else:
            print("✅ Successfully bypassed market hours restriction!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure Ollama is running with HuiHui model")

if __name__ == "__main__":
    test_market_context() 