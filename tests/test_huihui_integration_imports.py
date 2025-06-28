#!/usr/bin/env python3
"""
Test HuiHui Integration Import Updates
=====================================

This script tests that all import statements have been successfully updated
to use the new huihui_integration directory structure.

Author: EOTS v2.5 AI Architecture Division
"""

import sys
import traceback

def test_new_imports():
    """Test imports from the new HuiHui integration structure."""
    print("🧪 Testing New HuiHui Integration Imports...")
    print("=" * 50)
    
    tests = []
    
    # Test core imports
    try:
        from huihui_integration.core.model_interface import create_huihui_model
        tests.append(("✅", "huihui_integration.core.model_interface"))
    except ImportError as e:
        tests.append(("❌", f"huihui_integration.core.model_interface: {e}"))
    
    try:
        from huihui_integration.core.ai_model_router import AIRouter
        tests.append(("✅", "huihui_integration.core.ai_model_router"))
    except ImportError as e:
        tests.append(("❌", f"huihui_integration.core.ai_model_router: {e}"))
    
    try:
        from huihui_integration.core.local_llm_client import LocalLLMClient
        tests.append(("✅", "huihui_integration.core.local_llm_client"))
    except ImportError as e:
        tests.append(("❌", f"huihui_integration.core.local_llm_client: {e}"))
    
    # Test monitoring imports
    try:
        from huihui_integration.monitoring.usage_monitor import get_usage_monitor
        tests.append(("✅", "huihui_integration.monitoring.usage_monitor"))
    except ImportError as e:
        tests.append(("❌", f"huihui_integration.monitoring.usage_monitor: {e}"))
    
    try:
        from huihui_integration.monitoring.supabase_manager import get_supabase_manager
        tests.append(("✅", "huihui_integration.monitoring.supabase_manager"))
    except ImportError as e:
        tests.append(("❌", f"huihui_integration.monitoring.supabase_manager: {e}"))
    
    try:
        from huihui_integration.monitoring.safety_manager import get_safety_manager
        tests.append(("✅", "huihui_integration.monitoring.safety_manager"))
    except ImportError as e:
        tests.append(("❌", f"huihui_integration.monitoring.safety_manager: {e}"))
    
    # Test expert imports
    try:
        from huihui_integration.experts.market_regime import get_expert_info
        tests.append(("✅", "huihui_integration.experts.market_regime"))
    except ImportError as e:
        tests.append(("❌", f"huihui_integration.experts.market_regime: {e}"))
    
    try:
        from huihui_integration.experts.options_flow import get_expert_info
        tests.append(("✅", "huihui_integration.experts.options_flow"))
    except ImportError as e:
        tests.append(("❌", f"huihui_integration.experts.options_flow: {e}"))
    
    try:
        from huihui_integration.experts.sentiment import get_expert_info
        tests.append(("✅", "huihui_integration.experts.sentiment"))
    except ImportError as e:
        tests.append(("❌", f"huihui_integration.experts.sentiment: {e}"))
    
    # Test orchestrator bridge
    try:
        from huihui_integration.orchestrator_bridge import get_bridge_status
        tests.append(("✅", "huihui_integration.orchestrator_bridge"))
    except ImportError as e:
        tests.append(("❌", f"huihui_integration.orchestrator_bridge: {e}"))
    
    # Test main integration
    try:
        from huihui_integration import get_system_info
        tests.append(("✅", "huihui_integration (main)"))
    except ImportError as e:
        tests.append(("❌", f"huihui_integration (main): {e}"))
    
    # Print results
    for status, test_name in tests:
        print(f"{status} {test_name}")
    
    # Summary
    passed = sum(1 for status, _ in tests if status == "✅")
    total = len(tests)
    print(f"\n📊 Results: {passed}/{total} imports successful")
    
    return passed == total

def test_file_cleanup():
    """Test that obsolete files have been properly removed."""
    print("\n🧹 Testing File Cleanup...")
    print("=" * 50)

    import os

    obsolete_files = [
        "utils/huihui_pydantic_model.py",
        "utils/ai_model_router.py",
        "utils/local_llm_client.py",
        "utils/huihui_usage_monitor.py",
        "utils/huihui_supabase_manager.py",
        "utils/huihui_safety_manager.py",
        "utils/huihui_security_manager.py",
        "utils/huihui_feedback_system.py"
    ]

    tests = []

    for file_path in obsolete_files:
        if os.path.exists(file_path):
            tests.append(("❌", f"{file_path} still exists (should be removed)"))
        else:
            tests.append(("✅", f"{file_path} properly removed"))

    # Print results
    for status, test_name in tests:
        print(f"{status} {test_name}")

    # Summary
    passed = sum(1 for status, _ in tests if status == "✅")
    total = len(tests)
    print(f"\n📊 Results: {passed}/{total} files properly cleaned up")

    return passed == total

def test_system_functionality():
    """Test that the HuiHui integration system is functional."""
    print("\n🚀 Testing System Functionality...")
    print("=" * 50)
    
    try:
        # Test main system info
        from huihui_integration import get_system_info, is_system_ready
        
        system_info = get_system_info()
        print(f"✅ System Version: {system_info['version']}")
        print(f"✅ Available Experts: {system_info['experts_available']}")
        print(f"✅ System Ready: {is_system_ready()}")
        
        # Test expert status
        from huihui_integration.experts import get_expert_status
        expert_status = get_expert_status()
        print(f"✅ Expert Status: {expert_status['available_count']}/3 experts available")
        
        # Test monitoring status
        from huihui_integration.monitoring import get_monitoring_status
        monitoring_status = get_monitoring_status()
        print(f"✅ Monitoring System: {monitoring_status['status']['monitoring_initialized']}")
        
        return True
        
    except Exception as e:
        print(f"❌ System functionality test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all import tests."""
    print("🧠 HuiHui Integration Import Test Suite")
    print("=" * 60)
    
    # Run tests
    new_imports_ok = test_new_imports()
    cleanup_ok = test_file_cleanup()
    functionality_ok = test_system_functionality()
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 FINAL SUMMARY")
    print("=" * 60)
    
    if new_imports_ok:
        print("✅ New HuiHui integration imports: WORKING")
    else:
        print("❌ New HuiHui integration imports: FAILED")

    if cleanup_ok:
        print("✅ File cleanup: COMPLETE")
    else:
        print("❌ File cleanup: INCOMPLETE")

    if functionality_ok:
        print("✅ System functionality: WORKING")
    else:
        print("❌ System functionality: FAILED")

    if all([new_imports_ok, cleanup_ok, functionality_ok]):
        print("\n🎉 ALL TESTS PASSED! HuiHui integration migration is complete!")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
