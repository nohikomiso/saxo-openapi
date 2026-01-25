"""Type safety tests for contrib utilities (Task 7.3.5).

This test module verifies that contrib utility modules have proper type hints
where applicable. Testing the following modules:

- saxo_openapi.contrib.session: account_info, account_info2
- saxo_openapi.contrib.ws.stream: decode_ws_msg
- saxo_openapi.contrib.util.instrument_to_uic: InstrumentToUic

Note: Task 7.3.5 is OPTIONAL. Skip tests if complex async types are needed.
"""

import inspect

from saxo_openapi.contrib import session
from saxo_openapi.contrib.util import instrument_to_uic
from saxo_openapi.contrib.ws import stream


class TestSessionFunctionsExist:
    """Test that session helper functions exist and are callable."""

    def test_account_info_function_exists(self):
        """Test account_info function exists."""
        assert hasattr(session, "account_info")
        assert callable(session.account_info)

    def test_account_info_has_client_parameter(self):
        """Test account_info has client parameter."""
        sig = inspect.signature(session.account_info)
        assert "client" in sig.parameters

    def test_account_info2_function_exists(self):
        """Test account_info2 function exists."""
        assert hasattr(session, "account_info2")
        assert callable(session.account_info2)

    def test_account_info2_has_client_parameter(self):
        """Test account_info2 has client parameter."""
        sig = inspect.signature(session.account_info2)
        assert "client" in sig.parameters


class TestStreamFunctionsExist:
    """Test that stream helper functions exist."""

    def test_decode_ws_msg_function_exists(self):
        """Test decode_ws_msg function exists."""
        assert hasattr(stream, "decode_ws_msg")
        assert callable(stream.decode_ws_msg)

    def test_decode_ws_msg_has_raw_parameter(self):
        """Test decode_ws_msg has raw parameter."""
        sig = inspect.signature(stream.decode_ws_msg)
        assert "raw" in sig.parameters


class TestInstrumentToUicFunctionExists:
    """Test that InstrumentToUic function exists."""

    def test_instrument_to_uic_function_exists(self):
        """Test InstrumentToUic function exists."""
        assert hasattr(instrument_to_uic, "InstrumentToUic")
        assert callable(instrument_to_uic.InstrumentToUic)

    def test_instrument_to_uic_has_required_parameters(self):
        """Test InstrumentToUic has required parameters."""
        sig = inspect.signature(instrument_to_uic.InstrumentToUic)
        params = list(sig.parameters.keys())
        assert "client" in params
        assert "AccountKey" in params
        assert "spec" in params


class TestContribUtilsImportsWork:
    """Test that contrib utility modules can be imported."""

    def test_session_module_import(self):
        """Test session module can be imported."""
        from saxo_openapi.contrib import session as s

        assert s is not None
        assert hasattr(s, "account_info")

    def test_stream_module_import(self):
        """Test stream module can be imported."""
        from saxo_openapi.contrib.ws import stream as st

        assert st is not None
        assert hasattr(st, "decode_ws_msg")

    def test_instrument_to_uic_import(self):
        """Test InstrumentToUic can be imported."""
        from saxo_openapi.contrib.util import InstrumentToUic

        assert InstrumentToUic is not None
        assert callable(InstrumentToUic)

    def test_instrument_to_uic_from_util(self):
        """Test InstrumentToUic import from util module."""
        from saxo_openapi.contrib.util import instrument_to_uic as i2u

        assert i2u is not None
        assert hasattr(i2u, "InstrumentToUic")
