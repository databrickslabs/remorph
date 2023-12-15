import unittest
from io import StringIO
from unittest.mock import patch

import pytest

from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.helpers.validate import Validate


@pytest.mark.skip(reason="Not implemented yet")
class TestValidate(unittest.TestCase):
    def setUp(self):
        self.config = MorphConfig(
            source="snowflake",
            input_sql="input_sql",
            output_folder="output_folder",
            skip_validation=False,
            catalog_name="catalog",
            schema_name="schema",
        )
        self.validate = Validate()

    @patch.object(Validate, "query")
    def test_query_valid(self, mock_validate_query):
        mock_validate_query.return_value = (True, None)
        flag, exception = self.validate.query(
            "SELECT current_timestamp()", self.config.catalog_name, self.config.schema_name
        )
        self.assertTrue(flag)
        self.assertIsNone(exception)

    @patch.object(Validate, "query")
    def test_query_invalid(self, mock_validate_query):
        mock_validate_query.return_value = (True, "[TABLE_OR_VIEW_NOT_FOUND]")
        flag, exception = self.validate.query(
            "SELECT * FROM mockdb.mocktable", self.config.catalog_name, self.config.schema_name
        )
        self.assertTrue(flag)
        self.assertIsNotNone(exception)

    @patch.object(Validate, "validate_format_result")
    def test_validate_format_result_valid_query(self, mock_validate_format_result):
        output = "SELECT current_timestamp()"
        mock_validate_format_result.return_value = (output + "\n;\n", None)
        result, exception = self.validate.validate_format_result(self.config, output)
        self.assertEqual(result, output + "\n;\n")
        self.assertIsNone(exception)

    @patch.object(Validate, "validate_format_result")
    def test_validate_format_result_invalid_query(self, mock_validate_format_result):
        input_sql = "SELECT current_timestamps()"
        exception = "[UNRESOLVED_ROUTINE]"
        buffer = StringIO()
        buffer.write("-------------- Exception Start-------------------\n")
        buffer.write("/* \n")
        buffer.write(exception)
        buffer.write("\n */ \n")
        buffer.write(input_sql)
        buffer.write("\n ---------------Exception End --------------------\n")

        expected_result = buffer.getvalue()
        mock_validate_format_result.return_value = (expected_result, exception)
        result, exception = self.validate.validate_format_result(self.config, input_sql)
        self.assertEqual(result, expected_result)
        self.assertTrue("[UNRESOLVED_ROUTINE]" in exception)
