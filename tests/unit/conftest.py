import re
from pathlib import Path
from collections.abc import Sequence
from unittest.mock import create_autospec

import pytest
from sqlglot import ErrorLevel, UnsupportedError, Dialect
from sqlglot.errors import SqlglotError, ParseError
from sqlglot import parse_one as sqlglot_parse_one
from sqlglot import transpile


from databricks.labs.remorph.config import TranspileConfig
from databricks.labs.remorph.transpiler.sqlglot.dialect_utils import SQLGLOT_DIALECTS
from databricks.labs.remorph.transpiler.sqlglot.generator.databricks import Databricks
from databricks.labs.remorph.transpiler.sqlglot.parsers.snowflake import Snowflake
from databricks.sdk.core import Config

from .transpiler.helpers.functional_test_cases import (
    FunctionalTestFile,
    FunctionalTestFileWithExpectedException,
    expected_exceptions,
)


@pytest.fixture(scope="session")
def mock_databricks_config():
    yield create_autospec(Config)


@pytest.fixture()
def transpile_config():
    yield TranspileConfig(
        transpiler="sqlglot",
        source_dialect="snowflake",
        input_source="input_sql",
        output_folder="output_folder",
        sdk_config={"cluster_id": "test_cluster"},
        skip_validation=False,
        catalog_name="catalog",
        schema_name="schema",
        mode="current",
    )


# TODO Add Standardized Sql Formatter to python functional tests.
def _normalize_string(value: str) -> str:
    # Remove extra spaces and ensure consistent spacing around parentheses
    value = re.sub(r'\s+', ' ', value)  # Replace multiple spaces with a single space
    value = re.sub(r'\s*\(\s*', ' ( ', value)  # Ensure space around opening parenthesis
    value = re.sub(r'\s*\)\s*', ' ) ', value)  # Ensure space around closing parenthesis
    value = value.strip()  # Remove leading and trailing spaces
    # Remove indentations, trailing spaces from each line, and convert to lowercase
    lines = [line.rstrip() for line in value.splitlines()]
    return " ".join(lines).lower().strip()


@pytest.fixture
def normalize_string():
    return _normalize_string


def get_dialect(input_dialect: str) -> Dialect:
    value = SQLGLOT_DIALECTS.get(input_dialect)
    if isinstance(value, Dialect):
        return value
    if isinstance(value, type(Dialect)):
        return value()
    raise ValueError(f"Can't instantiate dialect from {value}")


def parse_one(sql):
    dialect = Databricks
    return sqlglot_parse_one(sql, read=dialect)


def validate_source_transpile(databricks_sql, *, source=None, pretty=False, experimental=False):
    """
    Validate that:
    1. Everything in `source` transpiles to `databricks_sql`

    Args:
        databricks_sql (str): Main SQL expression
        source (dict): Mapping of dialect -> SQL
        pretty (bool): prettify the output
        experimental (bool): experimental flag False by default
    """

    for source_dialect, source_sql in (source or {}).items():
        write_dialect = get_dialect("experimental") if experimental else get_dialect("databricks")

        actual_sql = "; ".join(
            transpile(
                source_sql,
                read=get_dialect(source_dialect),
                write=write_dialect,
                pretty=pretty,
                error_level=None,
            )
        )
        orig_sql = actual_sql
        actual_sql = _normalize_string(actual_sql.rstrip(';'))
        expected_sql = _normalize_string(databricks_sql.rstrip(';'))

        error_msg = f"""-> *target_sql* `{expected_sql}` is not matching with\
                                \n-> *transpiled_sql* `{actual_sql}`\
                                \n-> for *source_dialect* `{source_dialect}\
        ORIG:
{orig_sql}
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
                transpile(
                    target_sql, read=Snowflake, write=get_dialect(target_dialect), pretty=pretty, error_level=None
                )[0]
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


_ANTLR_CORE_FOLDER = 'core_engine'


def parse_sql_files(input_dir: Path, source: str, target: str, is_expected_exception):
    suite: list[FunctionalTestFile | FunctionalTestFileWithExpectedException] = []
    for filenames in input_dir.rglob("*.sql"):
        # Skip files in the core directory
        if _ANTLR_CORE_FOLDER in filenames.parts:
            continue
        with open(filenames, 'r', encoding="utf-8") as file_content:
            content = file_content.read()
            source_pattern = rf'--\s*{source} sql:\n(.*?)(?=\n--\s*{target} sql:|$)'
            target_pattern = rf'--\s*{target} sql:\n(.*)'

            # Extract source and target queries

            source_match = re.search(source_pattern, content, re.DOTALL)
            target_match = re.search(target_pattern, content, re.DOTALL)

            source_sql = source_match.group(1).strip().rstrip(";") if source_match else ""
            target_sql = target_match.group(1).strip() if target_match else ""

            # when multiple sqls are present below target
            test_name = filenames.name.replace(".sql", "")
            if is_expected_exception:
                exception_type = expected_exceptions.get(test_name, SqlglotError)
                exception = SqlglotError(test_name)
                if exception_type in {ParseError, UnsupportedError}:
                    exception = exception_type(test_name)
                suite.append(
                    FunctionalTestFileWithExpectedException(
                        target_sql,
                        source_sql,
                        test_name,
                        exception,
                        target,
                    )
                )
            else:
                suite.append(FunctionalTestFile(target_sql, source_sql, test_name, target))
    return suite


def get_functional_test_files_from_directory(
    input_dir: Path, source: str, target: str, is_expected_exception=False
) -> Sequence[FunctionalTestFileWithExpectedException]:
    """Get all functional tests in the input_dir."""
    suite = parse_sql_files(input_dir, source, target, is_expected_exception)
    return suite


@pytest.fixture
def expr():
    return parse_one("SELECT col1 FROM DUAL")


def path_to_resource(*args: str) -> str:
    resource_path = Path(__file__).parent.parent / "resources"
    for arg in args:
        resource_path = resource_path / arg
    return str(resource_path)
