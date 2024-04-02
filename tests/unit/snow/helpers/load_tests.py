import os
from pathlib import Path

from tests.unit.snow.helpers.functional_test_files import FunctionalTestFile


def get_functional_test_files_from_directory(input_dir: Path | str) -> list[FunctionalTestFile]:
    """Get all functional tests in the input_dir."""
    suite = []
    for dirpath, _, filenames in os.walk(input_dir):
        if dirpath.endswith("__pycache__"):
            continue
        for file in filenames:
            if file.endswith('.sql'):
                abs_path = Path(dirpath) / file
                with open(abs_path, 'r', encoding="utf-8") as file_content:
                    content = file_content.read()

            parts = content.split('-- source:')
            for part in parts[1:]:
                source, databricks_sql = part.split('-- databricks_sql:')
                source = source.strip().rstrip(';')
                databricks_sql = databricks_sql.strip().rstrip(';').replace('\\', '')
                test_name = file.replace('.sql', '')
                suite.append(FunctionalTestFile(databricks_sql, source, test_name))
    for item in suite:
        print(item.test_name)
    return suite


get_functional_test_files_from_directory(
    '/Users/kushagra.parashar/IdeaProjects/remorph/tests/resources/functional/snowflake'
)
