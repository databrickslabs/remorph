# Logic for processing test cases with expected exceptions, can be removed if not needed.
from pathlib import Path

import pytest

from tests.unit.snow.helpers.functional_test_cases import (
    FunctionalTestFileWithExpectedException,
)
from tests.unit.snow.test_databricks import parse_sql_files


def get_functional_test_files_from_directory_ee(input_dir: Path | str) -> list[FunctionalTestFileWithExpectedException]:
    # We pass the second parameter as True because we have expected exceptions
    suite = parse_sql_files(input_dir, True)
    return suite


path_expected_exceptions = Path('tests/resources/functional/snowflake_expected_exceptions')
functional_tests_expected_exceptions = get_functional_test_files_from_directory_ee(path_expected_exceptions)
test_names_expected_exceptions = [f.test_name for f in functional_tests_expected_exceptions]


@pytest.mark.parametrize("sample", functional_tests_expected_exceptions, ids=test_names_expected_exceptions)
def test_databricks_expected_exceptions(dialect_context, sample: FunctionalTestFileWithExpectedException):
    validate_source_transpile, _ = dialect_context
    with pytest.raises(sample.expected_exception):
        validate_source_transpile(databricks_sql=sample.databricks_sql, source={"snowflake": sample.source})
