"""Unit Tests for OpenAPI Lookup Package."""
import unittest


class TestOpenAPILookup(unittest.TestCase):
    """OpenAPI Lookup Unit Tests."""

    def test_import_successful(self) -> None:
        """Test import of openapi_lookup package."""
        try:
            import openapi_lookup  # noqa: F401

        except ImportError:
            self.fail("Failed to import openapi_lookup package.")
