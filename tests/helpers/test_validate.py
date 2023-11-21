import unittest

from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.helpers.validate import Validate


class TestValidate(unittest.TestCase):
    def setUp(self):
        self.config = MorphConfig(
            source="snowflake",
            input_sql="input_sql",
            output_folder="output_folder",
            skip_validation="false",
            validation_mode="LOCAL_REMOTE",
            catalog_nm="catalog",
            schema_nm="schema",
        )
        self.validate = Validate(connection_mode="LOCAL_REMOTE")

    def test_query_valid(self):
        flag, exception = self.validate.query(
            "SELECT current_timestamp()", self.config.catalog_nm, self.config.schema_nm
        )
        self.assertTrue(flag)
        self.assertIsNone(exception)

    def test_query_invalid(self):
        flag, exception = self.validate.query(
            "SELECT * FROM mockdb.mocktable", self.config.catalog_nm, self.config.schema_nm
        )
        self.assertTrue(flag)
        self.assertIsNotNone(exception)

    def test_validate_format_result_valid_query(self):
        output = "SELECT current_timestamp()"
        result, exception = self.validate.validate_format_result(self.config, output)
        self.assertEqual(result, output + "\n;\n")
        self.assertIsNone(exception)

    def test_validate_format_result_invalid_query(self):
        input_sql = "SELECT current_timestamps()"
        result, exception = self.validate.validate_format_result(self.config, input_sql)
        query = input_sql
        expected_result = (
            "-------------- Exception Start-------------------\n"
            "/* \n" + exception + "\n */ \n" + query + "\n ---------------Exception End --------------------\n"
        )
        self.assertEqual(result, expected_result)
        self.assertTrue("[UNRESOLVED_ROUTINE]" in exception)


if __name__ == "__main__":
    unittest.main()
