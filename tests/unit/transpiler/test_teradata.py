from pathlib import Path

import pytest

from ..conftest import FunctionalTestFile, get_functional_test_files_from_directory

path = Path(__file__).parent / Path('../../resources/functional/teradata/ddl/')
functional_tests = get_functional_test_files_from_directory(path, "teradata", "databricks", False)
test_names = [f.test_name for f in functional_tests]


@pytest.mark.parametrize("sample", functional_tests, ids=test_names)
def test_teradata(dialect_context, sample: FunctionalTestFile):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(databricks_sql=sample.databricks_sql, source={"teradata": sample.source}, pretty=True)
