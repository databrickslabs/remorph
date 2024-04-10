import os
from pathlib import Path

import pytest

from tests.unit.snow.helpers.functional_test_cases import (
    FunctionalTestFile,
    FunctionalTestFileWithExpectedException,
    expected_exceptions,
)


def parse_sql_files(input_dir: Path, is_expected_exception=False):
    suite = []
    for dirpath, _, filenames in os.walk(input_dir):
        if dirpath.endswith("__pycache__"):
            continue
        for file in filenames:
            if file.endswith('.sql'):
                abs_path = Path(dirpath) / file
                with open(abs_path, 'r', encoding="utf-8") as file_content:
                    content = file_content.read()
            if content:
                parts = content.split('-- snowflake sql:')
                for part in parts[1:]:
                    source, databricks_sql = part.split('-- databricks sql:')
                    source = source.strip().rstrip(';')
                    databricks_sql = databricks_sql.strip().rstrip(';').replace('\\', '')
                    test_name = file.replace('.sql', '')

                    if is_expected_exception:
                        suite.append(
                            FunctionalTestFileWithExpectedException(
                                databricks_sql, source, test_name, expected_exceptions[test_name]
                            )
                        )
                    else:
                        suite.append(FunctionalTestFile(databricks_sql, source, test_name))

    return suite


def get_functional_test_files_from_directory(input_dir: Path | str) -> list[FunctionalTestFile]:
    """Get all functional tests in the input_dir."""
    suite = parse_sql_files(input_dir)
    return suite


path = Path('tests/resources/functional/snowflake/')
functional_tests = get_functional_test_files_from_directory(path)
test_names = [f.test_name for f in functional_tests]


@pytest.mark.parametrize("sample", functional_tests, ids=test_names)
def test_databricks(dialect_context, sample: FunctionalTestFile):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(databricks_sql=sample.databricks_sql, source={"snowflake": sample.source})
