from tests.unit.snow.test_dialect import Validator


class TestSnowflake(Validator):
    """
    Test Class to validate Snowflake dialect
    """

    dialect = "snowflake"

    def test_parse_parameter(self):
        """
        Function to assert conversion from source: `snowflake(read)` to target: `Databricks(sql)`
        """
        sql = """SELECT DISTINCT
  ABC,
  CAST('${SCHEMA_NM}_MV' AS STRING),
  sys_dt,
  ins_ts,
  upd_ts
FROM ${SCHEMA_NM}_MV.${TBL_NM}
WHERE
  NOT xyz IS NULL AND src_ent = '${SCHEMA_NM}_MV.COL'"""

        self.validate_all_transpiled(
            sql,
            read={
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

    def test_decimal_keyword(self):
        """
        Function to test dec as alias name
        """

        sql = """SELECT
  dec.id,
  dec.key,
  xy.value
FROM table AS dec
JOIN table2 AS xy
  ON dec.id = xy.id"""

        self.validate_all_transpiled(
            sql,
            read={
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
