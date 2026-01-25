"""Test cases for gap analysis updates based on official Saxo Bank OpenAPI documentation."""

from saxo_openapi.endpoints.accounthistory import accountvalues
from saxo_openapi.endpoints.portfolio import netpositions, users
from saxo_openapi.endpoints.rootservices import sessions


class TestAccountHistoryUpdates:
    """Test AccountHistory updates based on gap analysis."""

    def test_performance_v4_path(self):
        """Test that performance v4 endpoint is available."""
        # According to gap analysis: hist/v3/perf -> hist/v4/performance
        # The old v3 path should still exist but might be deprecated
        # New v4 path should be available as well
        from saxo_openapi.endpoints.accounthistory import performance_v4

        # Test that v4 endpoint exists
        assert hasattr(performance_v4, "AccountPerformanceV4")
        endpoint_v4 = performance_v4.AccountPerformanceV4("dummy_key")
        assert "hist/v4/performance" in endpoint_v4._endpoint


class TestRootServicesUpdates:
    """Test RootServices updates based on gap analysis."""

    def test_session_capabilities_method(self):
        """Test that ChangeSessionCapabilities uses PATCH instead of PUT."""
        # According to gap analysis: PUT root/v1/sessions/capabilities -> PATCH
        assert hasattr(sessions, "ChangeSessionCapabilities")
        endpoint = sessions.ChangeSessionCapabilities(data={})
        # Check that the method is PATCH instead of PUT
        assert endpoint.method == "PATCH", f"Expected PATCH but got {endpoint.method}"


class TestAccountValuesPath:
    """Test AccountValues path correction."""

    def test_account_values_path_case(self):
        """Test that account values path uses lowercase 'v'."""
        # According to gap analysis: accountValues -> accountvalues
        assert hasattr(accountvalues, "AccountSummary")
        endpoint = accountvalues.AccountSummary("dummy_key")
        # Check that the endpoint contains 'accountvalues' not 'accountValues'
        assert "accountvalues" in endpoint._endpoint
        assert "accountValues" not in endpoint._endpoint


class TestPortfolioUpdates:
    """Test Portfolio updates based on gap analysis."""

    def test_users_entitlements_endpoints(self):
        """Test that users endpoint has entitlements endpoints."""
        # According to gap analysis:
        # - GET port/v1/users/me/entitlements
        # - GET port/v1/users/{UserKey}/entitlements
        assert hasattr(users, "UsersMeEntitlements"), "Missing UsersMeEntitlements endpoint"
        assert hasattr(users, "UsersEntitlements"), "Missing UsersEntitlements endpoint"

    def test_netpositions_delete_endpoint(self):
        """Test that netpositions has DELETE subscription endpoint."""
        # According to gap analysis:
        # - DELETE port/v1/netpositions/subscriptions/{ContextId}/{ReferenceId}
        assert hasattr(netpositions, "NetPositionSubscriptionRemoveById"), "Missing NetPositionSubscriptionRemoveById endpoint"


class TestTradeUpdates:
    """Test Trade updates based on gap analysis."""

    def test_multileg_orders_endpoints(self):
        """Test that multileg order endpoints exist."""
        # According to gap analysis, there should be multileg order endpoints
        # such as:
        # - POST trade/v2/orders/multileg
        # - POST trade/v2/orders/multileg/precheck
        # - GET trade/v2/orders/multileg/defaults
        from saxo_openapi.endpoints.trading import multilegorders

        assert hasattr(multilegorders, "MultilegOrder")
        assert hasattr(multilegorders, "MultilegOrderPrecheck")
        assert hasattr(multilegorders, "MultilegOrderDefaults")

        # Test endpoints
        order_endpoint = multilegorders.MultilegOrder(data={})
        assert order_endpoint.method == "POST"
        assert "trade/v2/orders/multileg" in order_endpoint._endpoint

        precheck_endpoint = multilegorders.MultilegOrderPrecheck(data={})
        assert precheck_endpoint.method == "POST"
        assert "trade/v2/orders/multileg/precheck" in precheck_endpoint._endpoint

        defaults_endpoint = multilegorders.MultilegOrderDefaults(params={})
        assert defaults_endpoint.method == "GET"
        assert "trade/v2/orders/multileg/defaults" in defaults_endpoint._endpoint

    def test_multileg_prices_endpoints(self):
        """Test that multileg price endpoints exist."""
        # According to gap analysis:
        # - POST trade/v1/prices/multileg
        # - POST trade/v1/prices/multileg/subscriptions
        from saxo_openapi.endpoints.trading import multilegprices

        assert hasattr(multilegprices, "MultilegPrice")
        assert hasattr(multilegprices, "MultilegPriceSubscription")

        # Test endpoints
        price_endpoint = multilegprices.MultilegPrice(data={})
        assert price_endpoint.method == "POST"
        assert "trade/v1/prices/multileg" in price_endpoint._endpoint

        sub_endpoint = multilegprices.MultilegPriceSubscription(data={})
        assert sub_endpoint.method == "POST"
        assert "trade/v1/prices/multileg/subscriptions" in sub_endpoint._endpoint

    def test_additional_trade_endpoints(self):
        """Test additional trade endpoints mentioned in gap analysis."""
        # - GET trade/v1/allocationkeys/distributions/{AllocationKeyId}
        # - GET trade/v1/infoprices/list/anonymous
        # - PUT trade/v1/prices/subscriptions/{ContextId}/{ReferenceId}/MarginImpact
        # - POST trade/v2/trades

        from saxo_openapi.endpoints.trading import (
            allocationkeys,
            infoprices,
            prices_extensions,
            trades,
        )

        # Test allocation key distributions
        assert hasattr(allocationkeys, "GetAllocationKeyDistributions")
        dist_endpoint = allocationkeys.GetAllocationKeyDistributions("alloc_key")
        assert "trade/v1/allocationkeys/distributions" in dist_endpoint._endpoint

        # Test anonymous info prices
        assert hasattr(infoprices, "AnonymousInfoPrices")
        anon_endpoint = infoprices.AnonymousInfoPrices(params={})
        assert "trade/v1/infoprices/list/anonymous" in anon_endpoint._endpoint

        # Test margin impact subscription
        assert hasattr(prices_extensions, "MarginImpactSubscription")
        margin_endpoint = prices_extensions.MarginImpactSubscription("ctx", "ref", data={})
        assert margin_endpoint.method == "PUT"
        assert "MarginImpact" in margin_endpoint._endpoint

        # Test trades endpoint
        assert hasattr(trades, "Trade")
        trade_endpoint = trades.Trade(data={})
        assert trade_endpoint.method == "POST"
        assert "trade/v2/trades" in trade_endpoint._endpoint


class TestMarketDataDocumentsUpdates:
    """Test MarketData Documents updates based on gap analysis."""

    def test_instrument_documents_paths(self):
        """Test that market data document endpoints exist and have correct paths."""
        from saxo_openapi.endpoints.marketdata import documents

        # Test InstrumentPdfDocument endpoint
        assert hasattr(documents, "InstrumentPdfDocument"), "Missing InstrumentPdfDocument endpoint"
        pdf = documents.InstrumentPdfDocument(Uic=1234, AssetType="Stock")
        assert "mkt/v2/instruments" in pdf._endpoint
        assert "documents/pdf" in pdf._endpoint

        # Test RecommendedInstrumentDocuments endpoint
        assert hasattr(documents, "RecommendedInstrumentDocuments"), "Missing RecommendedInstrumentDocuments endpoint"
        rec = documents.RecommendedInstrumentDocuments(Uic=1234, AssetType="Stock")
        assert "mkt/v2/instruments" in rec._endpoint
        assert "documents/recommended" in rec._endpoint


def test_all_gap_analysis_updates():
    """Run all gap analysis update tests."""
    # Test all implemented gap analysis updates
    root_test = TestRootServicesUpdates()
    root_test.test_session_capabilities_method()

    account_values_test = TestAccountValuesPath()
    account_values_test.test_account_values_path_case()

    portfolio_test = TestPortfolioUpdates()
    portfolio_test.test_users_entitlements_endpoints()
    portfolio_test.test_netpositions_delete_endpoint()

    trade_test = TestTradeUpdates()
    trade_test.test_multileg_orders_endpoints()
    trade_test.test_multileg_prices_endpoints()
    trade_test.test_additional_trade_endpoints()

    history_test = TestAccountHistoryUpdates()
    history_test.test_performance_v4_path()

    # Test MarketData Documents
    marketdata_test = TestMarketDataDocumentsUpdates()
    marketdata_test.test_instrument_documents_paths()
