# pylint: disable=wrong-import-order,ungrouped-imports, useless-suppression)
import os
from pathlib import Path
from unittest.mock import create_autospec

import pytest
from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config
from databricks.sdk.service import iam
from sqlglot import ErrorLevel, UnsupportedError
from sqlglot import parse_one as sqlglot_parse_one
from sqlglot import transpile

from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.snow.databricks import Databricks
from databricks.labs.remorph.snow.snowflake import Snow

from .snow.helpers.functional_test_cases import (
    FunctionalTestFile,
    FunctionalTestFileWithExpectedException,
    expected_exceptions,
)


@pytest.fixture(scope="session")
def mock_spark_session():
    spark = create_autospec(DatabricksSession)
    yield spark


@pytest.fixture(scope="session")
def mock_databricks_config():
    yield create_autospec(Config)


@pytest.fixture()
def mock_workspace_client():
    client = create_autospec(WorkspaceClient)
    client.current_user.me = lambda: iam.User(user_name="remorph", groups=[iam.ComplexValue(display="admins")])
    yield client


@pytest.fixture()
def morph_config():
    yield MorphConfig(
        sdk_config={"cluster_id": "test_cluster"},
        source="snowflake",
        input_sql="input_sql",
        output_folder="output_folder",
        skip_validation=False,
        catalog_name="catalog",
        schema_name="schema",
        mode="current",
    )


def _normalize_string(value: str) -> str:
    # Remove indentations and convert to lowercase
    lines = [line.strip() for line in value.splitlines()]
    return " ".join(lines).lower().strip()


@pytest.fixture
def normalize_string():
    return _normalize_string


def get_dialect(input_dialect=None):
    match input_dialect:
        case "databricks":
            return Databricks
        case "snowflake":
            return Snow
        case _:
            return input_dialect


def parse_one(sql):
    dialect = Databricks
    return sqlglot_parse_one(sql, read=dialect)


def validate_source_transpile(databricks_sql, *, source=None, pretty=False):
    """
    Validate that:
    1. Everything in `source` transpiles to `databricks_sql`

    Args:
        databricks_sql (str): Main SQL expression
        source (dict): Mapping of dialect -> SQL
        pretty (bool): prettify the output
    """

    for source_dialect, source_sql in (source or {}).items():
        actual_sql = _normalize_string(
            transpile(source_sql, read=get_dialect(source_dialect), write=Databricks, pretty=pretty, error_level=None)[
                0
            ]
        ).rstrip(';')

        expected_sql = _normalize_string(databricks_sql).rstrip(';')

        error_msg = f"""-> *target_sql* `{expected_sql}` is not matching with\
                                \n-> *transpiled_sql* `{actual_sql}`\
                                \n-> for *source_dialect* `{source_dialect}\
                             """

        assert expected_sql == actual_sql, error_msg


def validate_target_transpile(input_sql, *, target=None, pretty=False):
    """
    Validate that:
    1. `target_sql` transpiles to `input_sql` using `target` dialect

    Args:
        input_sql (str): Main SQL expression
        target (dict): Mapping of dialect -> SQL
        pretty (bool): prettify the output
    """
    expression = parse_one(input_sql) if input_sql else None
    for target_dialect, target_sql in (target or {}).items():
        if target_sql is UnsupportedError:
            with pytest.raises(UnsupportedError):
                if expression:
                    expression.sql(target_dialect, unsupported_level=ErrorLevel.RAISE)
        else:
            actual_sql = _normalize_string(
                transpile(target_sql, read=Snow, write=get_dialect(target_dialect), pretty=pretty, error_level=None)[0]
            )

            expected_sql = _normalize_string(input_sql)

            error_msg = f"""-> *target_sql* `{expected_sql}` is not matching with\
                                \n-> *transpiled_sql* `{actual_sql}`\
                                \n-> for *target_dialect* `{target_dialect}\
                             """

            assert expected_sql == actual_sql, error_msg


@pytest.fixture(scope="session")
def dialect_context():
    yield validate_source_transpile, validate_target_transpile


def parse_sql_files(input_dir: Path, source: str, target: str, is_expected_exception):
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
                parts = content.split(f'-- ${source.lower()} sql:')
                for part in parts[1:]:
                    source, databricks_sql = part.split(f'-- ${target.lower()} sql:')
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


def get_functional_test_files_from_directory(
    input_dir: Path | str, source: str, target: str, is_expected_exception=False
) -> list[FunctionalTestFile] | list[FunctionalTestFileWithExpectedException]:
    """Get all functional tests in the input_dir."""
    suite = parse_sql_files(input_dir, source, target, is_expected_exception)
    return suite
