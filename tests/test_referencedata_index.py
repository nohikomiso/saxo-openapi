"""
ReferenceData endpoints の .ai/index.json 登録テスト

Phase 3-C1: ReferenceData Part 1 のエンドポイントが
.ai/index.json に正しく登録されていることを確認します。
"""

import json
from pathlib import Path

import pytest


def load_ai_index() -> dict:
    """Load .ai/index.json"""
    index_path = Path(__file__).parent.parent / ".ai" / "index.json"
    with open(index_path, encoding="utf-8") as f:
        return json.load(f)


class TestReferenceDataPart1Index:
    """ReferenceData Part 1 endpoints のインデックステスト"""

    @pytest.fixture
    def ai_index(self):
        return load_ai_index()

    def test_algostrategies_endpoints_registered(self, ai_index):
        """algostrategies エンドポイントが登録されていること"""
        endpoints = ai_index.get("endpoints", {})

        # AlgoStrategies endpoint
        assert "referencedata.algostrategies.AlgoStrategies" in endpoints, "AlgoStrategies endpoint not found in index"

        algo_strategies = endpoints["referencedata.algostrategies.AlgoStrategies"]
        assert algo_strategies["category"] == "referencedata"
        assert algo_strategies["subcategory"] == "algostrategies"
        assert algo_strategies["method"] == "GET"
        assert algo_strategies["path"] == "openapi/ref/v1/algostrategies/"
        assert "docs" in algo_strategies
        assert algo_strategies["docs"] == "docs/api/referencedata/algostrategies.md#algostrategies"

        # AlgoStrategyDetails endpoint
        assert "referencedata.algostrategies.AlgoStrategyDetails" in endpoints, "AlgoStrategyDetails endpoint not found in index"

        algo_details = endpoints["referencedata.algostrategies.AlgoStrategyDetails"]
        assert algo_details["category"] == "referencedata"
        assert algo_details["subcategory"] == "algostrategies"
        assert algo_details["method"] == "GET"
        assert algo_details["path"] == "openapi/ref/v1/algostrategies/{Name}"

    def test_countries_endpoint_registered(self, ai_index):
        """countries エンドポイントが登録されていること"""
        endpoints = ai_index.get("endpoints", {})

        assert "referencedata.countries.Countries" in endpoints, "Countries endpoint not found in index"

        countries = endpoints["referencedata.countries.Countries"]
        assert countries["category"] == "referencedata"
        assert countries["subcategory"] == "countries"
        assert countries["method"] == "GET"
        assert countries["path"] == "openapi/ref/v1/countries/"
        assert countries["docs"] == "docs/api/referencedata/countries.md#countries"

    def test_cultures_endpoint_registered(self, ai_index):
        """cultures エンドポイントが登録されていること"""
        endpoints = ai_index.get("endpoints", {})

        assert "referencedata.cultures.Cultures" in endpoints, "Cultures endpoint not found in index"

        cultures = endpoints["referencedata.cultures.Cultures"]
        assert cultures["category"] == "referencedata"
        assert cultures["subcategory"] == "cultures"
        assert cultures["method"] == "GET"
        assert cultures["path"] == "openapi/ref/v1/cultures/"
        assert cultures["docs"] == "docs/api/referencedata/cultures.md#cultures"

    def test_currencies_endpoint_registered(self, ai_index):
        """currencies エンドポイントが登録されていること"""
        endpoints = ai_index.get("endpoints", {})

        assert "referencedata.currencies.Currencies" in endpoints, "Currencies endpoint not found in index"

        currencies = endpoints["referencedata.currencies.Currencies"]
        assert currencies["category"] == "referencedata"
        assert currencies["subcategory"] == "currencies"
        assert currencies["method"] == "GET"
        assert currencies["path"] == "openapi/ref/v1/currencies/"
        assert currencies["docs"] == "docs/api/referencedata/currencies.md#currencies"

    def test_metadata_updated(self, ai_index):
        """メタデータが更新されていること"""
        metadata = ai_index.get("metadata", {})

        # 少なくとも5つのエンドポイントが登録されているはず
        # (AlgoStrategies, AlgoStrategyDetails, Countries, Cultures, Currencies)
        actual_count = len(ai_index.get("endpoints", {}))
        assert metadata.get("total_endpoints") == actual_count, f"Metadata count ({metadata.get('total_endpoints')}) doesn't match actual ({actual_count})"

    def test_endpoint_structure_validity(self, ai_index):
        """エンドポイント構造が正しいこと"""
        endpoints = ai_index.get("endpoints", {})

        required_fields = [
            "category",
            "subcategory",
            "method",
            "path",
            "summary",
            "docs",
        ]

        for endpoint_key in [
            "referencedata.algostrategies.AlgoStrategies",
            "referencedata.algostrategies.AlgoStrategyDetails",
            "referencedata.countries.Countries",
            "referencedata.cultures.Cultures",
            "referencedata.currencies.Currencies",
        ]:
            if endpoint_key in endpoints:
                endpoint_data = endpoints[endpoint_key]
                for field in required_fields:
                    assert field in endpoint_data, f"{endpoint_key} missing required field: {field}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
