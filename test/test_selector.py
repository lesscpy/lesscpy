"""
Tests for CSS property.
"""
from lesscpy.lessc.parser import LessParser
from test.core import IntegrationTestCase


class TestSelector(IntegrationTestCase):
    """
    Tests for parsing of selectors.
    """

    def test_class_selector(self):
        """
        Simple selector.
        """
        self.assertParsedResult(
            """
            .pi-test {
                background-color: red;
            }
            """,
            """
            .pi-test {
              background-color: red;
            }
            """
            )

    def test_id_selector(self):
        """
        Selectors can include an id.
        """
        self.assertParsedResult(
            """
            #pi-test {
                background-color: red;
            }
            """,
            """
            #pi-test {
              background-color: red;
            }
            """
            )

    def test_dash_selector(self):
        """
        Selectors can include a dash.

        Under normal circumstances dom elements should not include a dash,
        but LESS upstream test include such a DOM element.
        """
        self.assertParsedResult(
            """
            pi-test {
                background-color: red;
            }
            """,
            """
            pi-test {
              background-color: red;
            }
            """
            )
