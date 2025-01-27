from pathlib import Path

import pytest

from ..conftest import FunctionalTestFile, get_functional_test_files_from_directory

path = Path(__file__).parent / Path('../../resources/functional/snowflake/')
functional_tests = get_functional_test_files_from_directory(path, "snowflake", "databricks", False)
test_names = [f.test_name for f in functional_tests]


@pytest.mark.parametrize("sample", functional_tests, ids=test_names)
def test_snowflake(dialect_context, sample: FunctionalTestFile):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(databricks_sql=sample.databricks_sql, source={"snowflake": sample.source}, pretty=True)




def test_parse_parameter(dialect_context):
    """
    Function to assert conversion from source: `snowflake(read)` to target: `Databricks(sql)`
    """
    validate_source_transpile, _ = dialect_context
    sql = """
             SELECT DISTINCT
                ABC,
                CAST('${SCHEMA_NM}_MV' AS STRING),
                sys_dt,
                ins_ts,
                upd_ts
             FROM ${SCHEMA_NM}_MV.${TBL_NM}
             WHERE
                 xyz IS NOT NULL AND src_ent = '${SCHEMA_NM}_MV.COL'
          """

    validate_source_transpile(
        databricks_sql=sql,
        source={
            "snowflake": """
                                SELECT  DISTINCT
                                    ABC,
                                    CAST('${SCHEMA_NM}_MV' AS VARCHAR(261)),
                                    sys_dt,
                                    ins_ts,
                                    upd_ts
                                FROM ${SCHEMA_NM}_MV.${TBL_NM} WHERE xyz IS NOT NULL  AND
                                    src_ent = '${SCHEMA_NM}_MV.COL';
                            """,
        },
        pretty=True,
    )


def test_decimal_keyword(dialect_context):
    """
    Function to test dec as alias name
    """
    validate_source_transpile, _ = dialect_context

    sql = """
             SELECT
                dec.id,
                dec.key,
                xy.value
             FROM table AS dec
             JOIN table2 AS xy
             ON dec.id = xy.id
          """

    validate_source_transpile(
        databricks_sql=sql,
        source={
            "snowflake": """
                           SELECT
                               dec.id,
                               dec.key,
                               xy.value
                           FROM table dec
                           JOIN table2 xy
                           ON dec.id = xy.id
                         """,
        },
        pretty=True,
    )
