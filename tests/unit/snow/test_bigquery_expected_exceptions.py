# Logic for processing test cases with expected exceptions, can be removed if not needed.
from pathlib import Path

import pytest

from ..conftest import (
    FunctionalTestFileWithExpectedException,
    get_functional_test_files_from_directory,
)

path_expected_exceptions = Path(__file__).parent / Path('../../resources/functional/bigquery_expected_exceptions/')
functional_tests_expected_exceptions = get_functional_test_files_from_directory(
    path_expected_exceptions, "bigquery", "databricks", True
)
test_names_expected_exceptions = [f.test_name for f in functional_tests_expected_exceptions]


@pytest.mark.parametrize("sample", functional_tests_expected_exceptions, ids=test_names_expected_exceptions)
def test_bigquery_expected_exceptions(dialect_context, sample: FunctionalTestFileWithExpectedException):
    validate_source_transpile, _ = dialect_context
    with pytest.raises(type(sample.expected_exception)):
        validate_source_transpile(databricks_sql=sample.databricks_sql, source={"bigquery": sample.source})
