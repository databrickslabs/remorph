import io
import re
from pathlib import Path
from collections.abc import Sequence
from unittest.mock import create_autospec

import pytest
import yaml
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    ArrayType,
    BooleanType,
    IntegerType,
    LongType,
    MapType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)
from sqlglot import ErrorLevel, UnsupportedError
from sqlglot.errors import SqlglotError, ParseError
from sqlglot import parse_one as sqlglot_parse_one
from sqlglot import transpile

from databricks.sdk.errors import NotFound

from databricks.labs.remorph.config import TranspileConfig
from databricks.labs.remorph.transpiler.sqlglot.dialect_utils import SQLGLOT_DIALECTS
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Filters,
    JdbcReaderOptions,
    Schema,
    Table,
    ColumnThresholds,
    Transformation,
    TableThresholds,
)
from databricks.labs.remorph.transpiler.sqlglot.generator.databricks import Databricks
from databricks.labs.remorph.transpiler.sqlglot.parsers.snowflake import Snowflake
from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config
from databricks.sdk.service import iam

from .transpiler.helpers.functional_test_cases import (
    FunctionalTestFile,
    FunctionalTestFileWithExpectedException,
    expected_exceptions,
)


@pytest.fixture(scope="session")
def mock_spark() -> SparkSession:
    """
    Method helps to create spark session
    :return: returns the spark session
    """
    return SparkSession.builder.appName("Remorph Reconcile Test").remote("sc://localhost").getOrCreate()


@pytest.fixture(scope="session")
def mock_databricks_config():
    yield create_autospec(Config)


@pytest.fixture()
def mock_workspace_client():
    client = create_autospec(WorkspaceClient)
    client.current_user.me = lambda: iam.User(user_name="remorph", groups=[iam.ComplexValue(display="admins")])
    yield client


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


def get_dialect(input_dialect=None):
    return SQLGLOT_DIALECTS.get(input_dialect)


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
def table_conf_mock():
    def _mock_table_conf(**kwargs):
        return Table(
            source_name="supplier",
            target_name="supplier",
            jdbc_reader_options=kwargs.get('jdbc_reader_options', None),
            join_columns=kwargs.get('join_columns', None),
            select_columns=kwargs.get('select_columns', None),
            drop_columns=kwargs.get('drop_columns', None),
            column_mapping=kwargs.get('column_mapping', None),
            transformations=kwargs.get('transformations', None),
            column_thresholds=kwargs.get('thresholds', None),
            filters=kwargs.get('filters', None),
        )

    return _mock_table_conf


@pytest.fixture
def table_conf_with_opts(column_mapping):
    return Table(
        source_name="supplier",
        target_name="target_supplier",
        jdbc_reader_options=JdbcReaderOptions(
            number_partitions=100, partition_column="s_nationkey", lower_bound="0", upper_bound="100"
        ),
        join_columns=["s_suppkey", "s_nationkey"],
        select_columns=["s_suppkey", "s_name", "s_address", "s_phone", "s_acctbal", "s_nationkey"],
        drop_columns=["s_comment"],
        column_mapping=column_mapping,
        transformations=[
            Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address_t)"),
            Transformation(column_name="s_phone", source="trim(s_phone)", target="trim(s_phone_t)"),
            Transformation(column_name="s_name", source="trim(s_name)", target="trim(s_name)"),
        ],
        column_thresholds=[
            ColumnThresholds(column_name="s_acctbal", lower_bound="0", upper_bound="100", type="int"),
        ],
        filters=Filters(source="s_name='t' and s_address='a'", target="s_name='t' and s_address_t='a'"),
        table_thresholds=[
            TableThresholds(lower_bound="0", upper_bound="100", model="mismatch"),
        ],
    )


@pytest.fixture
def column_mapping():
    return [
        ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
        ColumnMapping(source_name="s_address", target_name="s_address_t"),
        ColumnMapping(source_name="s_nationkey", target_name="s_nationkey_t"),
        ColumnMapping(source_name="s_phone", target_name="s_phone_t"),
        ColumnMapping(source_name="s_acctbal", target_name="s_acctbal_t"),
        ColumnMapping(source_name="s_comment", target_name="s_comment_t"),
    ]


@pytest.fixture
def table_schema():
    sch = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]

    sch_with_alias = [
        Schema("s_suppkey_t", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address_t", "varchar"),
        Schema("s_nationkey_t", "number"),
        Schema("s_phone_t", "varchar"),
        Schema("s_acctbal_t", "number"),
        Schema("s_comment_t", "varchar"),
    ]

    return sch, sch_with_alias


@pytest.fixture
def expr():
    return parse_one("SELECT col1 FROM DUAL")


@pytest.fixture
def report_tables_schema():
    recon_schema = StructType(
        [
            StructField("recon_table_id", LongType(), nullable=False),
            StructField("recon_id", StringType(), nullable=False),
            StructField("source_type", StringType(), nullable=False),
            StructField(
                "source_table",
                StructType(
                    [
                        StructField('catalog', StringType(), nullable=False),
                        StructField('schema', StringType(), nullable=False),
                        StructField('table_name', StringType(), nullable=False),
                    ]
                ),
                nullable=False,
            ),
            StructField(
                "target_table",
                StructType(
                    [
                        StructField('catalog', StringType(), nullable=False),
                        StructField('schema', StringType(), nullable=False),
                        StructField('table_name', StringType(), nullable=False),
                    ]
                ),
                nullable=False,
            ),
            StructField("report_type", StringType(), nullable=False),
            StructField("operation_name", StringType(), nullable=False),
            StructField("start_ts", TimestampType()),
            StructField("end_ts", TimestampType()),
        ]
    )

    metrics_schema = StructType(
        [
            StructField("recon_table_id", LongType(), nullable=False),
            StructField(
                "recon_metrics",
                StructType(
                    [
                        StructField(
                            "row_comparison",
                            StructType(
                                [
                                    StructField("missing_in_source", IntegerType()),
                                    StructField("missing_in_target", IntegerType()),
                                ]
                            ),
                        ),
                        StructField(
                            "column_comparison",
                            StructType(
                                [
                                    StructField("absolute_mismatch", IntegerType()),
                                    StructField("threshold_mismatch", IntegerType()),
                                    StructField("mismatch_columns", StringType()),
                                ]
                            ),
                        ),
                        StructField("schema_comparison", BooleanType()),
                    ]
                ),
            ),
            StructField(
                "run_metrics",
                StructType(
                    [
                        StructField("status", BooleanType(), nullable=False),
                        StructField("run_by_user", StringType(), nullable=False),
                        StructField("exception_message", StringType()),
                    ]
                ),
            ),
            StructField("inserted_ts", TimestampType(), nullable=False),
        ]
    )

    details_schema = StructType(
        [
            StructField("recon_table_id", LongType(), nullable=False),
            StructField("recon_type", StringType(), nullable=False),
            StructField("status", BooleanType(), nullable=False),
            StructField("data", ArrayType(MapType(StringType(), StringType())), nullable=False),
            StructField("inserted_ts", TimestampType(), nullable=False),
        ]
    )

    return recon_schema, metrics_schema, details_schema


def path_to_resource(*args: str) -> str:
    resource_path = Path(__file__).parent.parent / "resources"
    for arg in args:
        resource_path = resource_path / arg
    return str(resource_path)


@pytest.fixture
def mock_workspace_client_cli():
    state = {
        "/Users/foo/.remorph/config.yml": yaml.dump(
            {
                'version': 1,
                'catalog_name': 'transpiler',
                'schema_name': 'remorph',
                'transpiler': 'sqlglot',
                'source_dialect': 'snowflake',
                'sdk_config': {'cluster_id': 'test_cluster'},
            }
        ),
        "/Users/foo/.remorph/recon_config.yml": yaml.dump(
            {
                'version': 1,
                'source_schema': "src_schema",
                'target_catalog': "src_catalog",
                'target_schema': "tgt_schema",
                'tables': [
                    {
                        "source_name": 'src_table',
                        "target_name": 'tgt_table',
                        "join_columns": ['id'],
                        "jdbc_reader_options": None,
                        "select_columns": None,
                        "drop_columns": None,
                        "column_mapping": None,
                        "transformations": None,
                        "thresholds": None,
                        "filters": None,
                    }
                ],
                'source_catalog': "src_catalog",
            }
        ),
    }

    def download(path: str) -> io.StringIO | io.BytesIO:
        if path not in state:
            raise NotFound(path)
        if ".csv" in path:
            return io.BytesIO(state[path].encode('utf-8'))
        return io.StringIO(state[path])

    workspace_client = create_autospec(WorkspaceClient)
    workspace_client.current_user.me().user_name = "foo"
    workspace_client.workspace.download = download
    config = create_autospec(Config)
    config.warehouse_id = None
    config.cluster_id = None
    workspace_client.config = config
    return workspace_client
