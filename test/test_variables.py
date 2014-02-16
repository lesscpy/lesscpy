"""
Test for variables.

http://lesscss.org/features/#features-overview-feature
"""
from lesscpy.lessc.parser import LessParser
from test.core import IntegrationTestCase


class TestVariables(IntegrationTestCase):
    """
    Integration tests for variables.
    """

    def test_not_included(self):
        """
        Variables are not included in the parsed result but values
        are expanded in specific rules.

        http://lesscss.org/features/#variables-feature-overview
        """
        self.assertParsedResult(
            """
            @nice-blue: #5B83AD;
            @light-blue: @nice-blue + #111;

            #header {
              color: @light-blue;
            }
            """,
            """
            #header {
              color: #6c94be;
            }
            """
            )

    def test_interpolation_selector(self):
        """
        It can be used in selector names.

        http://lesscss.org/features/#variables-feature-selectors
        """
        self.assertParsedResult(
            """
            @mySelector: banner;

            .@{mySelector} {
              font-weight: bold;
              line-height: 40px;
              margin: 0 auto;
            }
            """,
            """
            .banner {
              font-weight: bold;
              line-height: 40px;
              margin: 0 auto;
            }
            """
            )


    def test_interpolation_url(self):
        """
        It can be used in urls.

        http://lesscss.org/features/#variables-feature-urls
        """
        self.assertParsedResult(
            """
            @images: "../img";

            body {
              color: #444444;
              background: url("@{images}/white-sand.png");
            }
            """,
            """
            body {
              color: #444444;
              background: url("../img/white-sand.png");
            }
            """
            )


    def test_interpolation_import(self):
        """
        It can be used in imports.

        http://lesscss.org/features/#variables-feature-import-statements
        """
        self.assertParsedResult(
            """
            @theme: "name";
            @import "@{theme}.less";
            """,
            """
            """
            )

    def test_interpolation_property(self):
        """
        It can be used in property name.

        http://lesscss.org/features/#variables-feature-properties
        """
        self.assertParsedResult(
            """
            @property: color;

            .widget {
              @{property}: #0ee;
              background-@{property}: #999;
            }
            """,
            """
            .widget {
              color: #0ee;
              background-color: #999;
            }
            """
            )

    def test_interpolation_variable_names(self):
        """
        It is also possible to define variables with a variable name.

        http://lesscss.org/features/#variables-feature-variable-names
        """
        self.assertParsedResult(
            """
            @fnord:  "I am fnord.";
            @var:    "fnord";
            .class {
              content: @@var;
            }
            """,
            """
            .class {
              content: "I am fnord.";
            }
            """
            )

    def test_lazy_loading(self):
        """
        Variables are lazy loaded and do not have to be declared before being
        used.
        """
        self.assertParsedResult(
            """
            .lazy-eval {
              width: @var;
            }

            @var: @a;
            @a: 9%;
            """,
            """
            .lazy-eval {
              width: 9%;
            }
            """
            )

    def test_lazy_loading_scope(self):
        """
        Variables are lazy loaded and do not have to be declared before being
        used.
        """
        self.assertParsedResult(
            """
            @var: 0;
            .class1 {
              @var: 1;
              .class {
                @var: 2;
                three: @var;
                @var: 3;
              }
              one: @var;
            }
            """,
            """
            .class1 .class {
              three: 3;
            }
            .class {
              one: 1;
            }
            """
            )

    def test_lazy_default_variables(self):
        """
        Variables can be overrided by putting the definition afterwards.

        http://lesscss.org/features/#variables-feature-default-variables
        """
        self.assertParsedResult(
            """
            // library
            @base-color: green;
            @dark-color: darken(@base-color, 10%);

            // use of library
            @base-color: red;

            .class {
                background: @base-color;
                text-color: @dark-color;
            }
            """,
            """
            .class {
              background: red;
              text-color: #cc0000;
            }
            """
            )
