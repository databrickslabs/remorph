from unittest.mock import MagicMock, Mock, create_autospec, patch

import pytest
from databricks.connect import DatabricksSession
from pyspark.sql.utils import AnalysisException, ParseException

from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.helpers.validate import Validate


class TestValidate:
    @pytest.fixture
    def spark_session(self):
        spark = create_autospec(DatabricksSession.builder.getOrCreate())
        yield spark

    @pytest.fixture
    def morph_config(self):
        yield MorphConfig(
            source="snowflake",
            input_sql="input_sql",
            output_folder="output_folder",
            skip_validation=False,
            catalog_name="catalog",
            schema_name="schema",
        )

    @patch("databricks.labs.remorph.helpers.validate.DatabricksSession")
    def test_valid_query(self, spark_session):
        validator = Validate()
        validator.spark = spark_session
        query = "SELECT * FROM a_table"
        result, exception = validator.query(query)
        spark_session.sql.assert_called()
        assert result is True
        assert exception is None

    @patch("databricks.labs.remorph.helpers.validate.DatabricksSession")
    def test_valid_query_with_explicit_catalog(self, spark_session):
        validator = Validate()
        validator.spark = spark_session
        query = "SELECT * FROM a_table"
        result, exception = validator.query(query, catalog_name="c_name", schema_name="s_name")
        spark_session.sql.assert_called()
        assert result is True
        assert exception is None

    @patch("databricks.labs.remorph.helpers.validate.DatabricksSession")
    def test_query_with_syntax_error(self, spark_session):
        validator = Validate()
        validator.spark = spark_session
        validator.spark.sql = MagicMock(side_effect=ParseException("[Syntax error]"))
        query = "SELECT * a_table"
        result, exception = validator.query(query)
        spark_session.sql.assert_called()
        assert result is False
        assert "[Syntax error]" in exception

    @patch("databricks.labs.remorph.helpers.validate.DatabricksSession")
    def test_query_with_analysis_error(self, spark_session):
        error_types = [
            ("[TABLE_OR_VIEW_NOT_FOUND]", True),
            ("[TABLE_OR_VIEW_ALREADY_EXISTS]", True),
            ("[UNRESOLVED_ROUTINE]", False),
            ("Hive support is required to CREATE Hive TABLE (AS SELECT).;", True),
            ("Some other analysis error", False),
        ]

        for err, status in error_types:
            validator = Validate()
            validator.spark = spark_session
            validator.spark.sql = MagicMock(side_effect=AnalysisException(err))
            query = "SELECT * FROM a_table"
            result, exception = validator.query(query)
            spark_session.sql.assert_called()
            assert result is status
            assert err in exception

    @patch("databricks.labs.remorph.helpers.validate.DatabricksSession")
    def test_query_with_error(self, spark_session):
        validator = Validate()
        validator.spark = spark_session
        validator.spark.sql = MagicMock(side_effect=Exception("[Some error]"))
        query = "SELECT * FROM a_table"
        result, exception = validator.query(query)
        spark_session.sql.assert_called()
        assert result is False
        assert "[Some error]" in exception

    @patch("databricks.labs.remorph.helpers.validate.DatabricksSession")
    def test_validate_format_result_with_valid_query(self, spark_session, morph_config):
        validator = Validate()
        validator.spark = spark_session
        query = "SELECT current_timestamp()"
        result, exception = validator.validate_format_result(morph_config, query)
        spark_session.sql.assert_called()
        assert query in result
        assert exception is None

    @patch("databricks.labs.remorph.helpers.validate.DatabricksSession")
    def test_validate_format_result_with_invalid_query(self, spark_session, morph_config):
        validator = Validate()
        validator.spark = spark_session
        validator.query = Mock()
        validator.query.return_value = (False, "[UNRESOLVED_ROUTINE]")
        input_query = "SELECT fn() FROM tab"
        result, exception = validator.validate_format_result(morph_config, input_query)
        assert "Exception Start" in result
        assert "[UNRESOLVED_ROUTINE]" in exception
