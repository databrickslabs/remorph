from unittest.mock import patch

import pytest

from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.transpiler.execute import morph


class TestExecuteMethods:
    # Fixture for a sample MorphConfig object with no validation
    @pytest.fixture
    def sample_config_no_validation(self):
        return MorphConfig(
            input_sql="input.sql",
            output_folder="output",
            source="source",
            skip_validation=False,
        )

    # Fixture for a sample MorphConfig object with validation
    @pytest.fixture
    def sample_config_with_validation(self):
        return MorphConfig(
            input_sql="input.sql",
            output_folder="output",
            source="source",
            skip_validation=True,
        )

    def test_morph(self, sample_config_no_validation):
        with patch("pathlib.Path.is_file", return_value=True), patch(
            "databricks.labs.remorph.helpers.file_utils.is_sql_file", return_value=True
        ), patch("databricks.labs.remorph.transpiler.execute.process_file", return_value=(1, [], [])):
            # Call the function
            status = morph(sample_config_no_validation)

        # Add assertions based on your code behavior
        assert status[0]["total_files_processed"] == 1
        assert status[0]["total_queries_processed"] == 1
        assert not status[0]["no_of_sql_failed_while_parsing"]
        assert not status[0]["no_of_sql_failed_while_validating"]
        assert status[0]["error_log_file"] == "None"
