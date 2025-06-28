"""
Consolidated AI Systems Integration Test v2.5
============================================

Comprehensive test suite for the consolidated AI systems:
1. MCP Unified Manager (replaces intelligence + tool orchestrators)
2. Enhanced Memory Intelligence (replaces memory + persistent engines)
3. AI Dashboard Intelligence (replaces ATIF insights generator)
4. Integration with ITS Orchestrator

This test verifies that all consolidated systems work together seamlessly
and provide enhanced intelligence capabilities with recursive learning.

Author: EOTS v2.5 Development Team - "Integration Testing Division"
Version: 2.5.0 - "CONSOLIDATED SYSTEM VERIFICATION"
"""

import pytest
import asyncio
import logging
from datetime import datetime
from unittest.mock import Mock
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import consolidated systems
from core_analytics_engine.mcp_unified_manager_v2_5 import MCPUnifiedManagerV2_5
# Legacy unified_ai_intelligence_system_v2_5 has been deprecated and replaced by HuiHui AI
# from core_analytics_engine.unified_ai_intelligence_system_v2_5 import (
#     UnifiedAIIntelligenceSystemV2_5,
#     get_unified_ai_intelligence_system
# )
from dashboard_application.modes.ai_dashboard.intelligence import generate_unified_ai_insights
from data_models.bundle_schemas import FinalAnalysisBundleV2_5
from data_models.processed_data import ProcessedUnderlyingAggregatesV2_5

logger = logging.getLogger(__name__)

class TestConsolidatedAISystems:
    """Test suite for consolidated AI systems."""
    
    @pytest.fixture
    def mock_config_manager(self):
        """Mock configuration manager."""
        config = Mock()
        config.config.system_settings.enable_unified_orchestrator = True
        return config
    
    @pytest.fixture
    def mock_database_manager(self):
        """Mock database manager."""
        db = Mock()
        db.get_memory_patterns.return_value = []
        db.store_memory_entity.return_value = True
        db.store_memory_relation.return_value = True
        db.store_memory_observation.return_value = True
        return db
    
    @pytest.fixture
    def sample_processed_data(self):
        """Sample processed data bundle."""
        underlying_data = ProcessedUnderlyingAggregatesV2_5(
            symbol="SPY",
            timestamp=datetime.now(),
            vapi_fa_z_score_und=1.5,
            dwfd_z_score_und=-0.8,
            tw_laf_z_score_und=2.1,
            gib_oi_based_und=0.3,
            a_dag_und=0.7,
            vri_2_0_und=1.2,
            current_market_regime_v2_5="BULLISH_MOMENTUM"
        )
        
        return ProcessedDataBundleV2_5(
            underlying_data_enriched=underlying_data,
            symbol="SPY",
            timestamp=datetime.now(),
            processing_timestamp=datetime.now()
        )
    
    @pytest.fixture
    def sample_final_bundle(self, sample_processed_data):
        """Sample final analysis bundle."""
        return FinalAnalysisBundleV2_5(
            processed_data_bundle=sample_processed_data,
            atif_recommendations_v2_5=None,
            news_intelligence_v2_5=None,
            key_levels_data_v2_5=KeyLevelsDataV2_5(timestamp=datetime.now()),
            system_status_messages=[],
            bundle_timestamp=datetime.now(),
            target_symbol="SPY"
        )
    
    def test_mcp_unified_manager_initialization(self, mock_config_manager):
        """Test MCP Unified Manager initialization."""
        try:
            manager = MCPUnifiedManagerV2_5(
                config_manager=mock_config_manager,
                eots_data_dir="test_data_cache"
            )
            
            assert manager is not None
            assert hasattr(manager, 'mcp_configs')
            assert hasattr(manager, 'pydantic_ai_enabled')
            assert len(manager.mcp_configs) > 0
            
            logger.info("✅ MCP Unified Manager initialization test passed")
            
        except Exception as e:
            pytest.fail(f"MCP Unified Manager initialization failed: {str(e)}")
    
    def test_enhanced_memory_intelligence_initialization(self, mock_config_manager, mock_database_manager):
        """Test Enhanced Memory Intelligence initialization."""
        try:
            memory_engine = EnhancedMemoryIntelligenceV2_5(
                config_manager=mock_config_manager,
                database_manager=mock_database_manager,
                memory_db_path="test_memory.db"
            )
            
            assert memory_engine is not None
            assert hasattr(memory_engine, 'pydantic_ai_enabled')
            assert hasattr(memory_engine, 'entity_cache')
            assert hasattr(memory_engine, 'relation_cache')
            
            logger.info("✅ Enhanced Memory Intelligence initialization test passed")
            
        except Exception as e:
            pytest.fail(f"Enhanced Memory Intelligence initialization failed: {str(e)}")
    
    def test_ai_dashboard_intelligence_function(self, sample_final_bundle):
        """Test AI Dashboard Intelligence function."""
        try:
            insights = generate_unified_ai_insights(sample_final_bundle, "SPY")
            
            assert isinstance(insights, list)
            assert len(insights) > 0
            assert all(isinstance(insight, str) for insight in insights)
            
            logger.info(f"✅ AI Dashboard Intelligence test passed - Generated {len(insights)} insights")
            
        except Exception as e:
            pytest.fail(f"AI Dashboard Intelligence test failed: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_mcp_unified_manager_intelligence_generation(self, mock_config_manager, sample_final_bundle):
        """Test MCP Unified Manager intelligence generation."""
        try:
            manager = MCPUnifiedManagerV2_5(
                config_manager=mock_config_manager,
                eots_data_dir="test_data_cache"
            )
            
            # Test intelligence generation (without actual MCP servers)
            intelligence = await manager.generate_unified_intelligence(sample_final_bundle, "SPY")
            
            assert isinstance(intelligence, dict)
            assert 'symbol' in intelligence
            assert 'unified_insights' in intelligence
            assert 'overall_confidence' in intelligence
            assert intelligence['symbol'] == "SPY"
            
            logger.info("✅ MCP Unified Manager intelligence generation test passed")
            
        except Exception as e:
            pytest.fail(f"MCP intelligence generation test failed: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_enhanced_memory_pattern_storage(self, mock_config_manager, mock_database_manager, sample_final_bundle):
        """Test Enhanced Memory Intelligence pattern storage."""
        try:
            memory_engine = EnhancedMemoryIntelligenceV2_5(
                config_manager=mock_config_manager,
                database_manager=mock_database_manager,
                memory_db_path="test_memory.db"
            )
            
            # Test pattern storage
            pattern_id = await memory_engine.store_enhanced_pattern(
                final_bundle=sample_final_bundle,
                symbol="SPY",
                additional_context={"test": "context"}
            )
            
            assert isinstance(pattern_id, str)
            assert len(pattern_id) > 0
            assert pattern_id in memory_engine.entity_cache
            
            logger.info(f"✅ Enhanced Memory pattern storage test passed - Pattern ID: {pattern_id}")
            
        except Exception as e:
            pytest.fail(f"Enhanced Memory pattern storage test failed: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_enhanced_memory_pattern_retrieval(self, mock_config_manager, mock_database_manager, sample_final_bundle):
        """Test Enhanced Memory Intelligence pattern retrieval."""
        try:
            memory_engine = EnhancedMemoryIntelligenceV2_5(
                config_manager=mock_config_manager,
                database_manager=mock_database_manager,
                memory_db_path="test_memory.db"
            )
            
            # Store a pattern first
            await memory_engine.store_enhanced_pattern(
                final_bundle=sample_final_bundle,
                symbol="SPY",
                additional_context={"test": "context"}
            )
            
            # Test pattern retrieval
            current_metrics = {
                "vapi_fa_z": 1.5,
                "dwfd_z": -0.8,
                "tw_laf_z": 2.1
            }
            
            market_conditions = {
                "regime": "BULLISH_MOMENTUM",
                "volatility_regime": "NORMAL"
            }
            
            similar_patterns = await memory_engine.find_similar_enhanced_patterns(
                current_metrics=current_metrics,
                symbol="SPY",
                market_conditions=market_conditions,
                limit=5
            )
            
            assert isinstance(similar_patterns, list)
            # Note: May be empty if no similar patterns found, which is OK for test
            
            logger.info(f"✅ Enhanced Memory pattern retrieval test passed - Found {len(similar_patterns)} patterns")
            
        except Exception as e:
            pytest.fail(f"Enhanced Memory pattern retrieval test failed: {str(e)}")
    
    def test_system_integration_imports(self):
        """Test that all consolidated systems can be imported together."""
        try:
            # Test all imports work together
            from core_analytics_engine.mcp_unified_manager_v2_5 import MCPUnifiedManagerV2_5
            # from core_analytics_engine.unified_ai_intelligence_system_v2_5 import UnifiedAIIntelligenceSystemV2_5  # DEPRECATED
            from dashboard_application.modes.ai_dashboard.intelligence import generate_unified_ai_insights
            
            logger.info("✅ System integration imports test passed")
            
        except ImportError as e:
            pytest.fail(f"System integration imports failed: {str(e)}")
    
    def test_pydantic_ai_availability(self):
        """Test Pydantic AI availability detection."""
        try:
            from core_analytics_engine.mcp_unified_manager_v2_5 import PYDANTIC_AI_AVAILABLE as mcp_ai
            # from core_analytics_engine.unified_ai_intelligence_system_v2_5 import PYDANTIC_AI_AVAILABLE as memory_ai  # DEPRECATED
            
            # Test MCP AI availability only (unified system deprecated)
            assert isinstance(mcp_ai, bool)
            
            logger.info(f"✅ Pydantic AI availability test passed - Available: {mcp_ai}")
            
        except Exception as e:
            pytest.fail(f"Pydantic AI availability test failed: {str(e)}")

def run_integration_tests():
    """Run integration tests manually."""
    print("🚀 Running Consolidated AI Systems Integration Tests...")
    
    # Create test instance
    test_suite = TestConsolidatedAISystems()
    
    # Mock objects
    mock_config = Mock()
    mock_config.config.system_settings.enable_unified_orchestrator = True
    
    mock_db = Mock()
    mock_db.get_memory_patterns.return_value = []
    mock_db.store_memory_entity.return_value = True
    
    # Sample data
    underlying_data = ProcessedUnderlyingAggregatesV2_5(
        symbol="SPY",
        timestamp=datetime.now(),
        vapi_fa_z_score_und=1.5,
        dwfd_z_score_und=-0.8,
        tw_laf_z_score_und=2.1,
        gib_oi_based_und=0.3,
        a_dag_und=0.7,
        vri_2_0_und=1.2,
        current_market_regime_v2_5="BULLISH_MOMENTUM"
    )
    
    processed_data = ProcessedDataBundleV2_5(
        underlying_data_enriched=underlying_data,
        symbol="SPY",
        timestamp=datetime.now(),
        processing_timestamp=datetime.now()
    )
    
    final_bundle = FinalAnalysisBundleV2_5(
        processed_data_bundle=processed_data,
        atif_recommendations_v2_5=None,
        news_intelligence_v2_5=None,
        key_levels_data_v2_5=KeyLevelsDataV2_5(timestamp=datetime.now()),
        system_status_messages=[],
        bundle_timestamp=datetime.now(),
        target_symbol="SPY"
    )
    
    try:
        # Run tests
        test_suite.test_system_integration_imports()
        test_suite.test_pydantic_ai_availability()
        test_suite.test_mcp_unified_manager_initialization(mock_config)
        test_suite.test_enhanced_memory_intelligence_initialization(mock_config, mock_db)
        test_suite.test_ai_dashboard_intelligence_function(final_bundle)
        
        # Run async tests
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        loop.run_until_complete(
            test_suite.test_mcp_unified_manager_intelligence_generation(mock_config, final_bundle)
        )
        
        loop.run_until_complete(
            test_suite.test_enhanced_memory_pattern_storage(mock_config, mock_db, final_bundle)
        )
        
        loop.run_until_complete(
            test_suite.test_enhanced_memory_pattern_retrieval(mock_config, mock_db, final_bundle)
        )
        
        loop.close()
        
        print("✅ All integration tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Integration tests failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_integration_tests()
    exit(0 if success else 1)
