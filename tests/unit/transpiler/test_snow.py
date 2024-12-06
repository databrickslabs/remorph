"""
    Test Cases to validate source Snowflake dialect
"""


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
