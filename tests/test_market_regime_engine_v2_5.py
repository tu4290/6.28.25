# tests/test_market_regime_engine_v2_5.py
# EOTS v2.5 - SENTRY-APPROVED CANONICAL SCRIPT
#
# This file contains comprehensive unit tests for the refactored
# MarketRegimeEngineV2_5, validating rule parsing, condition evaluation,
# and end-to-end regime classification.

from typing import Dict, Any
from datetime import datetime

import pytest
import pandas as pd
import numpy as np

from data_models.processed_data import (
    ProcessedDataBundleV2_5,
    ProcessedStrikeLevelMetricsV2_5,
    ProcessedUnderlyingAggregatesV2_5
)
from data_models.system_schemas import FinalAnalysisBundleV2_5
from data_models.context_schemas import DynamicThresholdsV2_5

from core_analytics_engine.market_regime_engine_v2_5 import MarketRegimeEngineV2_5, ParsedRule
from core_analytics_engine.eots_metrics.elite_definitions import MarketRegime

class MockConfigManager:
    """A mock ConfigManager that returns a predefined dictionary."""
    def __init__(self, config: Dict[str, Any]):
        self._config = config
    def get_setting(self, key: str):
        return self._config.get(key, {})

@pytest.fixture
def sample_data_bundle():
    """Provides a sample ProcessedDataBundleV2_5 for testing."""
    strike_metrics = [
        ProcessedStrikeLevelMetricsV2_5(strike=95.0, mspi=-0.8, sdag_multiplicative=-0.2),
        ProcessedStrikeLevelMetricsV2_5(strike=100.0, mspi=0.1, sdag_multiplicative=0.05),
        ProcessedStrikeLevelMetricsV2_5(strike=105.0, mspi=0.9, sdag_multiplicative=0.3),
    ]
    underlying_data = ProcessedUnderlyingAggregatesV2_5(
        symbol="TEST", timestamp=datetime.now(), price=100.5,
        gib_oi_based_und=-60e9,
        vapi_fa_z_score_und=2.5
    )
    return ProcessedDataBundleV2_5(
        strike_level_data_with_metrics=strike_metrics,
        underlying_data_enriched=underlying_data,
        processing_timestamp=datetime(2025, 6, 10, 15, 30, 0) # Afternoon
    )

def test_rule_parsing_success():
    """Verify correct parsing of valid rule configurations."""
    mock_config = {
        "market_regime_engine_settings": {
            "default_regime": "REGIME_DEFAULT",
            "regime_evaluation_order": ["REGIME_TEST"],
            "regime_rules": {
                "REGIME_TEST": [
                    {"metric": "gib_oi_based_und", "operator": "_lt", "value": -50000},
                    {"metric": "mspi", "operator": "_gt", "value": 0.5, "selector": "@ATM"},
                    {"metric": "sdag_multiplicative", "operator": "_lt", "value": -0.1, "aggregator": "mean"}
                ]
            }
        }
    }
    engine = MarketRegimeEngineV2_5(MockConfigManager(mock_config))

    # Test that rules were parsed correctly
    assert "REGIME_TEST" in engine._parsed_rules
    rules = engine._parsed_rules["REGIME_TEST"]
    assert len(rules) == 3

    # Test first rule
    rule1 = rules[0]
    assert rule1.metric == "gib_oi_based_und"
    assert rule1.operator == "_lt"
    assert rule1.value == -50000
    assert rule1.selector is None

    # Test second rule with selector
    rule2 = rules[1]
    assert rule2.metric == "mspi"
    assert rule2.operator == "_gt"
    assert rule2.value == 0.5
    assert rule2.selector == "@ATM"

    # Test third rule with aggregator
    rule3 = rules[2]
    assert rule3.metric == "sdag_multiplicative"
    assert rule3.operator == "_lt"
    assert rule3.value == -0.1
    assert rule3.aggregator == "mean"

def test_rule_parsing_failure():
    """Test that malformed rule configurations are handled gracefully."""
    mock_config = {
        "market_regime_engine_settings": {
            "default_regime": "REGIME_DEFAULT",
            "regime_evaluation_order": ["REGIME_TEST"],
            "regime_rules": {
                "REGIME_TEST": [
                    {"metric": "test_metric", "operator": "_invalid", "value": 1.0}  # Invalid operator
                ]
            }
        }
    }

    # The engine should initialize but log errors and have no valid rules
    engine = MarketRegimeEngineV2_5(MockConfigManager(mock_config))

    # Should have no valid parsed rules due to validation error
    assert "REGIME_TEST" in engine._parsed_rules
    assert len(engine._parsed_rules["REGIME_TEST"]) == 0

def test_evaluator_resolve_metric(sample_data_bundle):
    """Test the _RuleConditionEvaluator's ability to resolve metric values."""
    mock_config = {
        "market_regime_engine_settings": {
            "default_regime": "REGIME_DEFAULT",
            "regime_evaluation_order": [],
            "regime_rules": {}
        }
    }
    engine = MarketRegimeEngineV2_5(MockConfigManager(mock_config))
    evaluator = engine._RuleConditionEvaluator(sample_data_bundle, engine)

    # Test simple underlying lookup
    rule_gib = ParsedRule(regime_name="test", metric="gib_oi_based_und", operator="_lt", value="")
    assert evaluator._resolve_metric_value(rule_gib) == -60e9

    # Test aggregator
    rule_sdag_mean = ParsedRule(regime_name="test", metric="sdag_multiplicative", operator="_lt", value="", aggregator="mean")
    mean_val = evaluator._resolve_metric_value(rule_sdag_mean)
    assert np.isclose(mean_val, (-0.2 + 0.05 + 0.3) / 3)

    # Test selector
    rule_mspi_atm = ParsedRule(regime_name="test", metric="mspi", operator="_gt", value="", selector="@ATM")
    atm_val = evaluator._resolve_metric_value(rule_mspi_atm)
    assert atm_val is not None, "ATM selector should return a value"
    assert np.isclose(atm_val, 0.1) # Strike 100 is closest to price 100.5

async def test_regime_classification_scenario_1(sample_data_bundle):
    """Test scenario: GIB is very low, triggering a specific regime."""
    mock_config = {
        "market_regime_engine_settings": {
            "default_regime": "REGIME_DEFAULT",
            "regime_evaluation_order": ["REGIME_EXTREME_NEG_GIB"],
            "regime_rules": {
                "REGIME_EXTREME_NEG_GIB": [
                    {"metric": "gib_oi_based_und", "operator": "_lt", "value": -55e9}
                ]
            }
        }
    }
    engine = MarketRegimeEngineV2_5(MockConfigManager(mock_config))
    regime = await engine.determine_market_regime(sample_data_bundle)
    assert regime == "REGIME_EXTREME_NEG_GIB"
    
async def test_regime_classification_scenario_2(sample_data_bundle):
    """Test scenario: High VAPI triggers a different regime."""
    mock_config = {
        "market_regime_engine_settings": {
            "default_regime": "REGIME_DEFAULT",
            "regime_evaluation_order": ["REGIME_EXTREME_NEG_GIB", "REGIME_VAPI_SURGE_AFTERNOON"],
            "regime_rules": {
                "REGIME_EXTREME_NEG_GIB": [
                    {"metric": "gib_oi_based_und", "operator": "_lt", "value": -70e9}
                ],
                "REGIME_VAPI_SURGE_AFTERNOON": [
                    {"metric": "vapi_fa_z_score_und", "operator": "_gt", "value": 2.0}
                ]
            }
        }
    }
    engine = MarketRegimeEngineV2_5(MockConfigManager(mock_config))
    # Sample data has vapi_fa_z_score_und=2.5, which is > 2.0
    regime = await engine.determine_market_regime(sample_data_bundle)
    assert regime == "REGIME_VAPI_SURGE_AFTERNOON"

async def test_regime_classification_fallback_to_default(sample_data_bundle):
    """Test scenario: No rules match, falls back to the default regime."""
    mock_config = {
        "market_regime_engine_settings": {
            "default_regime": "REGIME_FALLBACK_SUCCESS",
            "regime_evaluation_order": ["REGIME_NON_MATCHING"],
            "regime_rules": {
                "REGIME_NON_MATCHING": [
                    {"metric": "gib_oi_based_und", "operator": "_gt", "value": 0}
                ]
            }
        }
    }
    engine = MarketRegimeEngineV2_5(MockConfigManager(mock_config))
    regime = await engine.determine_market_regime(sample_data_bundle)
    assert regime == "REGIME_FALLBACK_SUCCESS"