import logging
import os
from pathlib import Path

import pytest

from tests.unit.snow.helpers.functional_test_files import FunctionalTestFile


def get_functional_test_files_from_directory(input_dir: Path | str) -> list[FunctionalTestFile]:
    """Get all functional tests in the input_dir."""
    suite = []
    for dirpath, _, filenames in os.walk(input_dir):
        if dirpath.endswith("__pycache__"):
            continue
        for file in filenames:
            if file == '.DS_Store':
                continue
            if file.endswith('.sql'):
                abs_path = Path(dirpath) / file
                with open(abs_path, 'r', encoding="utf-8") as file_content:
                    content = file_content.read()
            if content:
                parts = content.split('-- source:')
                for part in parts[1:]:
                    source, databricks_sql = part.split('-- databricks_sql:')
                    source = source.strip().rstrip(';')
                    databricks_sql = databricks_sql.strip().rstrip(';').replace('\\', '')
                    test_name = file.replace('.sql', '')
                    suite.append(FunctionalTestFile(databricks_sql, source, test_name))


    return suite


path = Path('tests/resources/functional/snowflake')
functional_tests = get_functional_test_files_from_directory(path)
test_names = [f.test_name for f in functional_tests]


@pytest.mark.parametrize("sample", functional_tests, ids=test_names)
def test_databricks(dialect_context, sample: FunctionalTestFile):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(databricks_sql=sample.databricks_sql, source={"snowflake": sample.source})
