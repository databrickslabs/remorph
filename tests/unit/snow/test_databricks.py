from sqlglot import ParseError, UnsupportedError

from tests.unit.snow.test_dialect import Validator


class TestDatabricks(Validator):
    dialect = "databricks"

    def test_databricks(self):
        self.validate_identity("INSERT INTO a REPLACE WHERE cond VALUES (1), (2)")
        self.validate_identity("SELECT c1 : price")
        # [TODO] Fix the Return string when creating a function
        # self.validate_identity("CREATE FUNCTION a.b(x INT) RETURNS INT RETURN x + 1")
        self.validate_identity("CREATE FUNCTION a AS b")
        self.validate_identity("SELECT ${x} FROM ${y} WHERE ${z} > 1")
        self.validate_identity("CREATE TABLE foo (x DATE GENERATED ALWAYS AS (CAST(y AS DATE)))")

        self.validate_all(
            "CREATE TABLE foo (x INT GENERATED ALWAYS AS (YEAR(y)))",
            write={
                "databricks": "CREATE TABLE foo (x INT GENERATED ALWAYS AS (YEAR(TO_DATE(y))))",
            },
        )

    # https://docs.databricks.com/sql/language-manual/functions/colonsign.html
    def test_json(self):
        self.validate_identity("""SELECT c1 : price FROM VALUES ('{ "price": 5 }') AS T(c1)""")

        self.validate_all(
            """SELECT c1:['price'] FROM VALUES('{ "price": 5 }') AS T(c1)""",
            write={
                "databricks": """SELECT c1 : ARRAY('price') FROM VALUES ('{ "price": 5 }') AS T(c1)""",
            },
        )
        self.validate_all(
            """SELECT c1:item[1].price
            FROM VALUES('{ "item": [ { "model" : "basic", "price" : 6.12 }, { "model" : "medium", "price" : 9.24 } ] }')
            AS T(c1)""",
            write={
                "databricks": """SELECT c1 : item[1].price
                FROM
                VALUES ('{ "item": [ { "model" : "basic", "price" : 6.12 }, { "model" : "medium", "price" : 9.24 } ] }')
                AS T(c1)""",
            },
        )
        self.validate_all(
            """SELECT c1:item[*].price
            FROM
            VALUES('{ "item": [ { "model" : "basic", "price" : 6.12 }, { "model" : "medium", "price" : 9.24 } ] }')
            AS T(c1)""",
            write={
                "databricks": """SELECT c1 : item[*].price
                FROM
                VALUES ('{ "item": [ { "model" : "basic", "price" : 6.12 }, { "model" : "medium", "price" : 9.24 } ] }')
                AS T(c1)""",
            },
        )
        self.validate_all(
            """SELECT
            from_json(c1:item[*].price, 'ARRAY<DOUBLE>')[0]
            FROM VALUES('{ "item": [ { "model" : "basic", "price" : 6.12 }, { "model" : "medium", "price" : 9.24 } ] }')
            AS T(c1)""",
            write={
                "databricks": """SELECT
                FROM_JSON(c1 : item[*].price, 'ARRAY<DOUBLE>')[0]
                FROM
                VALUES ('{ "item": [ { "model" : "basic", "price" : 6.12 }, { "model" : "medium", "price" : 9.24 } ] }')
                AS T(c1)""",
            },
        )
        self.validate_all(
            """SELECT
            inline(from_json(c1:item[*], 'ARRAY<STRUCT<model STRING, price DOUBLE>>'))
            FROM VALUES('{ "item": [ { "model" : "basic", "price" : 6.12 }, { "model" : "medium", "price" : 9.24 } ] }')
            AS T(c1)""",
            write={
                "databricks": """SELECT
                INLINE(FROM_JSON(c1 : item[*], 'ARRAY<STRUCT<model STRING, price DOUBLE>>'))
                FROM
                VALUES ('{ "item": [ { "model" : "basic", "price" : 6.12 }, { "model" : "medium", "price" : 9.24 } ] }')
                AS T(c1)""",
            },
        )

    def test_datediff(self):
        self.validate_all(
            "SELECT DATEDIFF(year, 'start', 'end')",
            write={
                "tsql": "SELECT DATEDIFF(year, 'start', 'end')",
                "databricks": "SELECT DATEDIFF(year, 'start', 'end')",
            },
        )
        self.validate_all(
            "SELECT DATEDIFF(microsecond, 'start', 'end')",
            write={
                "databricks": "SELECT DATEDIFF(microsecond, 'start', 'end')",
                "postgres": "SELECT "
                "CAST(EXTRACT(epoch FROM CAST('end' AS TIMESTAMP) - CAST('start' AS TIMESTAMP)) * 1000000 "
                "AS BIGINT)",
            },
        )
        self.validate_all(
            "SELECT DATEDIFF(millisecond, 'start', 'end')",
            write={
                "databricks": "SELECT DATEDIFF(millisecond, 'start', 'end')",
                "postgres": "SELECT "
                "CAST(EXTRACT(epoch FROM CAST('end' AS TIMESTAMP) - CAST('start' AS TIMESTAMP)) * 1000 "
                "AS BIGINT)",
            },
        )
        self.validate_all(
            "SELECT DATEDIFF(second, 'start', 'end')",
            write={
                "databricks": "SELECT DATEDIFF(second, 'start', 'end')",
                "postgres": "SELECT "
                "CAST(EXTRACT(epoch FROM CAST('end' AS TIMESTAMP) - CAST('start' "
                "AS TIMESTAMP)) AS BIGINT)",
            },
        )
        self.validate_all(
            "SELECT DATEDIFF(minute, 'start', 'end')",
            write={
                "databricks": "SELECT DATEDIFF(minute, 'start', 'end')",
                "postgres": "SELECT "
                "CAST(EXTRACT(epoch FROM CAST('end' AS TIMESTAMP) - CAST('start' AS TIMESTAMP)) / 60 "
                "AS BIGINT)",
            },
        )
        self.validate_all(
            "SELECT DATEDIFF(hour, 'start', 'end')",
            write={
                "databricks": "SELECT DATEDIFF(hour, 'start', 'end')",
                "postgres": "SELECT "
                "CAST(EXTRACT(epoch FROM CAST('end' AS TIMESTAMP) - CAST('start' AS TIMESTAMP)) / 3600 "
                "AS BIGINT)",
            },
        )
        self.validate_all(
            "SELECT DATEDIFF(day, 'start', 'end')",
            write={
                "databricks": "SELECT DATEDIFF(day, 'start', 'end')",
                "postgres": "SELECT "
                "CAST(EXTRACT(epoch FROM CAST('end' AS TIMESTAMP) - CAST('start' AS TIMESTAMP)) / 86400 "
                "AS BIGINT)",
            },
        )
        self.validate_all(
            "SELECT DATEDIFF(week, 'start', 'end')",
            write={
                "databricks": "SELECT DATEDIFF(week, 'start', 'end')",
                "postgres": "SELECT "
                "CAST(EXTRACT(days FROM (CAST('end' AS TIMESTAMP) - CAST('start' AS TIMESTAMP))) / 7 "
                "AS BIGINT)",
            },
        )
        self.validate_all(
            "SELECT DATEDIFF(month, 'start', 'end')",
            write={
                "databricks": "SELECT DATEDIFF(month, 'start', 'end')",
                "postgres": "SELECT "
                "CAST(EXTRACT(year FROM AGE(CAST('end' AS TIMESTAMP), "
                "CAST('start' AS TIMESTAMP))) * 12 + EXTRACT(month FROM AGE(CAST('end' AS TIMESTAMP), "
                "CAST('start' AS TIMESTAMP))) AS BIGINT)",
            },
        )
        self.validate_all(
            "SELECT DATEDIFF(quarter, 'start', 'end')",
            write={
                "databricks": "SELECT DATEDIFF(quarter, 'start', 'end')",
                "postgres": "SELECT "
                "CAST(EXTRACT(year FROM AGE(CAST('end' AS TIMESTAMP), "
                "CAST('start' AS TIMESTAMP))) * 4 + EXTRACT(month FROM AGE(CAST('end' AS TIMESTAMP), "
                "CAST('start' AS TIMESTAMP))) / 3 AS BIGINT)",
            },
        )
        self.validate_all(
            "SELECT DATEDIFF(year, 'start', 'end')",
            write={
                "databricks": "SELECT DATEDIFF(year, 'start', 'end')",
                "postgres": "SELECT "
                "CAST(EXTRACT(year FROM AGE(CAST('end' AS TIMESTAMP), "
                "CAST('start' AS TIMESTAMP))) AS BIGINT)",
            },
        )
        # Test case to validate SF supported 'yrs' Date and Time Parts conversion
        self.validate_all_transpiled(
            "SELECT DATEDIFF(year, CAST('2021-02-28 12:00:00' AS TIMESTAMP), CAST('2021-03-28 12:00:00' AS TIMESTAMP))",
            write={
                "databricks": "SELECT datediff(yrs, TIMESTAMP'2021-02-28 12:00:00', TIMESTAMP'2021-03-28 12:00:00');",
            },
        )
        # Test case to validate SF supported 'years' Date and Time Parts conversion
        self.validate_all_transpiled(
            "SELECT DATEDIFF(year, CAST('2021-02-28 12:00:00' AS TIMESTAMP), CAST('2021-03-28 12:00:00' AS TIMESTAMP))",
            write={
                "databricks": "SELECT datediff(years, TIMESTAMP'2021-02-28 12:00:00', TIMESTAMP'2021-03-28 12:00:00');",
            },
        )
        # Test case to validate SF supported 'mm' Date and Time Parts conversion
        self.validate_all_transpiled(
            "SELECT DATEDIFF(month, CAST('2021-02-28' AS DATE), CAST('2021-03-28' AS DATE))",
            write={
                "databricks": "SELECT datediff(mm, DATE'2021-02-28', DATE'2021-03-28');",
            },
        )
        # Test case to validate SF supported 'mons' Date and Time Parts conversion
        self.validate_all_transpiled(
            "SELECT DATEDIFF(month, CAST('2021-02-28' AS DATE), CAST('2021-03-28' AS DATE))",
            write={
                "databricks": "SELECT datediff(mons, DATE'2021-02-28', DATE'2021-03-28');",
            },
        )
        # Test case to validate SF supported 'days' Date and Time Parts conversion
        self.validate_all_transpiled(
            "SELECT DATEDIFF(day, 'start', 'end')",
            write={
                "databricks": "SELECT datediff('days', 'start', 'end');",
            },
        )
        # Test case to validate SF supported 'dayofmonth' Date and Time Parts conversion
        self.validate_all_transpiled(
            "SELECT DATEDIFF(day, 'start', 'end')",
            write={
                "databricks": "SELECT datediff(dayofmonth, 'start', 'end');",
            },
        )
        # Test case to validate SF supported 'wk' Date and Time Parts conversion
        self.validate_all_transpiled(
            "SELECT DATEDIFF(week, 'start', 'end')",
            write={
                "databricks": "SELECT datediff(wk, 'start', 'end');",
            },
        )
        # Test case to validate SF supported 'woy' Date and Time Parts conversion
        self.validate_all_transpiled(
            "SELECT DATEDIFF(week, 'start', 'end')",
            write={
                "databricks": "SELECT datediff('woy', 'start', 'end');",
            },
        )
        # Test case to validate SF supported 'qtrs' Date and Time Parts conversion
        self.validate_all_transpiled(
            "SELECT DATEDIFF(quarter, 'start', 'end')",
            write={
                "databricks": "SELECT datediff('qtrs', 'start', 'end');",
            },
        )
        # Test case to validate SF supported 'quarters' Date and Time Parts conversion
        self.validate_all_transpiled(
            "SELECT DATEDIFF(quarter, 'start', 'end')",
            write={
                "databricks": "SELECT datediff(quarters, 'start', 'end');",
            },
        )
        self.validate_all_transpiled(
            "SELECT DATEDIFF(day, 'end', 'start')",
            write={"databricks": "SELECT DATEDIFF('start', 'end')"},
        )

    def test_add_date(self):
        self.validate_all(
            "SELECT DATEADD(year, 1, '2020-01-01')",
            write={
                "tsql": "SELECT DATEADD(year, 1, '2020-01-01')",
                "databricks": "SELECT DATEADD(year, 1, '2020-01-01')",
            },
        )
        self.validate_all_transpiled(
            "SELECT DATEADD(day, 'start', 'end')",
            write={"databricks": "SELECT DATEADD(days, 'start', 'end')"},
        )
        self.validate_all(
            "SELECT DATE_ADD('2020-01-01', 1)",
            write={
                "tsql": "SELECT DATEADD(DAY, 1, '2020-01-01')",
                "databricks": "SELECT DATEADD(DAY, 1, '2020-01-01')",
            },
        )

    def test_without_as(self):
        self.validate_all(
            "CREATE TABLE x (SELECT 1)",
            write={
                "databricks": "CREATE TABLE x AS (SELECT 1)",
            },
        )

        self.validate_all(
            "WITH x (select 1) SELECT * FROM x",
            write={
                "databricks": "WITH x AS (SELECT 1) SELECT * FROM x",
            },
        )

    def test_date_from_parts(self):
        self.validate_all_transpiled(
            """SELECT MAKE_DATE(1992, 6, 1)""",
            write={
                "databricks": """select date_from_parts(1992, 6, 1);""",
            },
        )
        self.validate_all_transpiled(
            """SELECT MAKE_DATE(2023, 10, 3), MAKE_DATE(2020, 4, 4)""",
            write={
                "databricks": """select date_from_parts(2023, 10, 3), date_from_parts(2020, 4, 4);""",
            },
        )

    def test_delete_from_keyword(self):
        self.validate_all(
            """DELETE FROM table AS a WHERE a.id IN (10, 20)""",
            write={
                "databricks": """DELETE FROM table AS a WHERE a.id IN (10, 20)""",
            },
        )
        self.validate_all(
            """DELETE FROM leased_bicycles USING (SELECT bicycle_ID AS bicycle_ID FROM returned_bicycles)
            AS returned WHERE leased_bicycles.bicycle_ID = returned.bicycle_ID;""",
            write={
                "databricks": """MERGE leased_bicycles USING (SELECT bicycle_ID AS bicycle_ID FROM returned_bicycles)
                AS returned ON leased_bicycles.bicycle_ID = returned.bicycle_ID WHEN MATCHED THEN DELETE;""",
            },
        )

        self.validate_all(
            """DELETE FROM leased_bicycles USING returned_bicycles
            WHERE leased_bicycles.bicycle_ID = returned_bicycles.bicycle_ID;""",
            write={
                "databricks": """MERGE leased_bicycles USING returned_bicycles
                ON leased_bicycles.bicycle_ID = returned_bicycles.bicycle_ID WHEN MATCHED THEN DELETE;""",
            },
        )

    def test_convert_timezone(self):
        # Test case to validate `convert_timezone` parsing with Src TZ, tgt TZ and String Timestamp
        self.validate_all_transpiled(
            """SELECT CONVERT_TIMEZONE('America/Los_Angeles', 'America/New_York', '2019-01-01 14:00:00') AS conv""",
            write={
                "databricks": """SELECT
                CONVERT_TIMEZONE('America/Los_Angeles', 'America/New_York', '2019-01-01 14:00:00'::timestamp_ntz)
                AS conv""",
            },
        )
        # Test case to validate `convert_timezone` parsing with tgt TZ and String Timestamp
        self.validate_all_transpiled(
            """SELECT CONVERT_TIMEZONE('America/Los_Angeles', '2018-04-05 12:00:00 +02:00') AS conv""",
            write={
                "databricks": """SELECT CONVERT_TIMEZONE('America/Los_Angeles', '2018-04-05 12:00:00 +02:00')
                AS conv""",
            },
        )
        # Test case to validate `convert_timezone` parsing with tgt TZ and Timestamp Column
        self.validate_all_transpiled(
            """SELECT a.col1, CONVERT_TIMEZONE('IST', a.ts_col) AS conv_ts FROM dummy AS a""",
            write={
                "databricks": """SELECT a.col1, CONVERT_TIMEZONE('IST', a.ts_col) AS conv_ts FROM dummy a""",
            },
        )
        # Test case to validate `convert_timezone` parsing with tgt TZ and Current Timestamp
        self.validate_all_transpiled(
            """SELECT
            CURRENT_TIMESTAMP() AS now_in_la, CONVERT_TIMEZONE('America/New_York', CURRENT_TIMESTAMP()) AS now_in_nyc,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP()) AS now_in_paris,
            CONVERT_TIMEZONE('Asia/Tokyo', CURRENT_TIMESTAMP()) AS now_in_tokyo""",
            write={
                "databricks": """SELECT CURRENT_TIMESTAMP() AS now_in_la,
                CONVERT_TIMEZONE('America/New_York', CURRENT_TIMESTAMP()) AS now_in_nyc,
                CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP()) AS now_in_paris,
                CONVERT_TIMEZONE('Asia/Tokyo', CURRENT_TIMESTAMP()) AS now_in_tokyo;""",
            },
        )
        # Test case to validate `convert_timezone` parsing with src TZ, tgt TZ and String converted to Timestamp column
        self.validate_all_transpiled(
            """SELECT CONVERT_TIMEZONE('Europe/Warsaw', 'UTC', '2019-01-01 00:00:00 +03:00')""",
            write={
                "databricks": """SELECT
                CONVERT_TIMEZONE('Europe/Warsaw', 'UTC', '2019-01-01 00:00:00 +03:00'::timestamp_ntz);""",
            },
        )

    def test_charindex(self):
        # Test case to validate CHARINDEX conversion
        self.validate_all_transpiled(
            """SELECT CHARINDEX('an', 'banana', 3), CHARINDEX('ab', 'abababab'), n, h, CHARINDEX(n, h) FROM pos""",
            write={
                "databricks": """select charindex('an', 'banana', 3),
                charindex('ab', 'abababab'), n, h, CHARINDEX(n, h) FROM pos;""",
            },
        )

    def test_dateadd(self):
        # Test case to validate `DATEADD` `DATE` conversion quoted unit 'day'
        self.validate_all_transpiled(
            """SELECT DATEADD(day, 3, CAST('2020-02-03' AS DATE))""",
            write={
                "databricks": """select dateadd('day', 3, '2020-02-03'::date);""",
            },
        )

    def test_is_integer(self):
        self.validate_all_transpiled(
            """SELECT
    CASE
       WHEN col IS NULL THEN NULL
       WHEN col RLIKE '^-?[0-9]+$' AND TRY_CAST(col AS INT) IS NOT NULL THEN TRUE
       ELSE FALSE
       END""",
            write={
                "databricks": "select IS_INTEGER(col);",
            },
        )

    def test_arrayagg(self):
        # Test case to validate `array_agg` conversion
        self.validate_all_transpiled(
            """SELECT ARRAY_AGG(O_ORDERKEY) FROM orders""",
            write={
                "databricks": """select array_agg(O_ORDERKEY) FROM orders;""",
            },
        )
        # Test case to validate `arrayagg` conversion
        self.validate_all_transpiled(
            """SELECT ARRAY_AGG(O_CLERK) FROM orders""",
            write={
                "databricks": """select arrayagg(O_CLERK) FROM orders;""",
            },
        )
        # Test case to validate `array_agg` tables columns conversion
        self.validate_all_transpiled(
            """SELECT ARRAY_AGG(O_ORDERSTATUS), ARRAY_AGG(O_COL) FROM orders""",
            write={
                "databricks": """select ARRAY_AGG(O_ORDERSTATUS), ARRAYAGG(O_COL) FROM orders;""",
            },
        )

    def test_arraycat(self):
        # Test case to validate `array_cat` conversion
        self.validate_all_transpiled(
            """SELECT CONCAT(col1, col2) FROM tbl""",
            write={
                "databricks": """select array_cat(col1, col2) FROM tbl;""",
            },
        )
        # Test case to validate `array_cat` conversion
        self.validate_all_transpiled(
            """SELECT CONCAT(ARRAY(1, 3), ARRAY(2, 4))""",
            write={
                "databricks": """select array_cat(array(1, 3), array(2, 4))""",
            },
        )

    def test_arraytostring(self):
        # Test case to validate `ARRAY_TO_STRING` conversion
        self.validate_all_transpiled(
            """SELECT ARRAY_JOIN(ary_column1, '') AS no_separation FROM tbl""",
            write={
                "databricks": "SELECT ARRAY_TO_STRING(ary_column1, '') AS no_separation FROM tbl",
            },
        )

    def test_listagg(self):
        # Test case to validate `listagg` conversion
        self.validate_all_transpiled(
            """SELECT ARRAY_JOIN(COLLECT_LIST(O_ORDERKEY), ' ') FROM orders WHERE O_TOTALPRICE > 450000""",
            write={
                "databricks": "SELECT listagg(O_ORDERKEY, ' ') FROM orders WHERE O_TOTALPRICE > 450000;",
            },
        )
        # Test case to validate `listagg` conversion
        self.validate_all_transpiled(
            """SELECT ARRAY_JOIN(COLLECT_LIST(O_ORDERSTATUS), '|') FROM orders WHERE O_TOTALPRICE > 450000""",
            write={
                "databricks": "SELECT listagg(O_ORDERSTATUS, '|') FROM orders WHERE O_TOTALPRICE > 450000;",
            },
        )

    def test_collate(self):
        self.validate_all_transpiled(
            "SELECT ENDSWITH(COLLATE('ñn', 'sp'), COLLATE('n', 'sp'))",
            write={
                "databricks": "SELECT ENDSWITH(COLLATE('ñn', 'sp'), COLLATE('n', 'sp'));",
            },
        )

        self.validate_all_transpiled(
            "SELECT v, COLLATION(v), COLLATE(v, 'sp-upper'), COLLATION(COLLATE(v, 'sp-upper')) FROM collation1",
            write={
                "databricks": "SELECT v, COLLATION(v), COLLATE(v, 'sp-upper'), COLLATION(COLLATE(v, 'sp-upper')) "
                "FROM collation1;",
            },
        )

    def test_tablesample(self):
        self.validate_all_transpiled(
            "SELECT * FROM (SELECT * FROM example_table) TABLESAMPLE (1 PERCENT) REPEATABLE (99)",
            write={
                "databricks": "select * from (select * from example_table) sample (1) seed (99);",
            },
        )

        self.validate_all_transpiled(
            "SELECT * FROM (SELECT * FROM example_table) TABLESAMPLE (1 PERCENT) REPEATABLE (99)",
            write={
                "databricks": "select * from (select * from example_table) tablesample (1) seed (99);",
            },
        )

        self.validate_all_transpiled(
            "SELECT * FROM (SELECT * FROM t1 JOIN t2 ON t1.a = t2.c) TABLESAMPLE (1 PERCENT)",
            write={
                "databricks": """
    select *
       from (
             select *
                from t1 join t2
                   on t1.a = t2.c
            ) sample (1);
                """,
            },
        )

    def test_skip_unsupported_operations(self):
        self.validate_all_transpiled(
            "",
            write={
                "databricks": "ALTER SESSION SET QUERY_TAG = 'tag1';",
            },
        )

        self.validate_all_transpiled(
            "",
            write={
                "databricks": "BEGIN;",
            },
        )

        self.validate_all_transpiled(
            "",
            write={
                "databricks": "ROLLBACK;",
            },
        )

        self.validate_all_transpiled(
            "",
            write={
                "databricks": "COMMIT;",
            },
        )

        self.validate_all_transpiled(
            "",
            write={
                "databricks": "CREATE STREAM mystream ON TABLE mytable;",
            },
        )

        self.validate_all_transpiled(
            "",
            write={
                "databricks": "ALTER STREAM mystream SET COMMENT = 'New comment for stream';",
            },
        )

        self.validate_all_transpiled(
            "",
            write={
                "databricks": "SHOW STREAMS LIKE 'line%' IN tpch.public;",
            },
        )

        self.validate_all_transpiled(
            "",
            write={
                "databricks": """
                CREATE TASK t1
                  SCHEDULE = '60 MINUTE'
                  TIMESTAMP_INPUT_FORMAT = 'YYYY-MM-DD HH24'
                  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL'
                AS
                INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);
                """,
            },
        )

        self.validate_all_transpiled(
            "",
            write={
                "databricks": "EXECUTE TASK mytask;",
            },
        )

        self.validate_all_transpiled(
            "SELECT DISTINCT dst.CREATED_DATE, dst.task_id, CAST(dd.delivery_id AS STRING) AS delivery_id, "
            "dst.ISSUE_CATEGORY, dst.issue, dd.store_id FROM proddb.public.dimension_salesforce_tasks AS dst JOIN "
            "edw.finance.dimension_deliveries AS dd ON dd.delivery_id = dst.delivery_id /* this ensures delivery_id "
            "is associated */ WHERE dst.mto_flag = 1 AND dst.customer_type IN ('Consumer') AND dd.STORE_ID IN (SELECT "
            "store_id FROM foo.bar.cng_stores_stage) AND dd.is_test = FALSE AND dst.origin IN ('Chat') AND NOT "
            "dd_agent_id IS NULL AND dst.CREATED_DATE > CURRENT_DATE - 7 ORDER BY 1 DESC NULLS FIRST, 3 DESC NULLS "
            "FIRST",
            write={
                "databricks": """
            SELECT DISTINCT
                dst.CREATED_DATE
                , dst.task_id
                , dd.delivery_id::TEXT AS delivery_id
                , dst.ISSUE_CATEGORY
                , dst.issue
                , dd.store_id
                FROM proddb.public.dimension_salesforce_tasks dst
                JOIN edw.finance.dimension_deliveries dd
                  ON dd.delivery_id = dst.delivery_id --this ensures delivery_id is associated
                WHERE dst.mto_flag = 1
                    AND dst.customer_type IN ('Consumer')
                    AND dd.STORE_ID IN (SELECT store_id FROM foo.bar.cng_stores_stage)
                    AND dd.is_test = FALSE
                    AND dst.origin IN ('Chat')
                    AND dd_agent_id IS NOT NULL
                AND dst.CREATED_DATE > current_date - 7
                ORDER BY 1 DESC, 3 DESC;
                """,
            },
        )

    def test_div0null(self):
        self.validate_all_transpiled(
            "SELECT IF(b = 0 OR b IS NULL, 0, a / b)",
            write={
                "databricks": "SELECT DIV0NULL(a, b)",
            },
        )

    def test_div0(self):
        self.validate_all_transpiled(
            "SELECT IF(b = 0, 0, a / b)",
            write={
                "databricks": "SELECT DIV0(a, b)",
            },
        )

    def test_bitor_agg(self):
        self.validate_all_transpiled(
            "SELECT BIT_OR(k) FROM bitwise_example",
            write={
                "databricks": "select bitor_agg(k) from bitwise_example",
            },
        )

        self.validate_all_transpiled(
            "SELECT s2, BIT_OR(k) FROM bitwise_example GROUP BY s2",
            write={
                "databricks": "select s2, bitor_agg(k) from bitwise_example group by s2",
            },
        )

    def test_coalesce(self):
        # Test case to validate `coalesce` conversion of column
        self.validate_all_transpiled(
            "SELECT COALESCE(col1, col2) AS coalesce_col FROM tabl",
            write={
                "databricks": "SELECT coalesce(col1, col2) AS coalesce_col FROM tabl;",
            },
        )

    def test_count(self):
        # Test case to validate `count` conversion of column
        self.validate_all_transpiled(
            "SELECT COUNT(col1) AS count_col1 FROM tabl",
            write={
                "databricks": "SELECT count(col1) AS count_col1 FROM tabl;",
            },
        )

    # [TODO]
    # Snowflake supports various date time parts
    # https://docs.snowflake.com/en/sql-reference/functions-date-time#label-supported-date-time-parts
    # Need to handle these in transpiler
    def test_date_trunc(self):
        # Test case to validate `date_trunc` conversion of static string
        self.validate_all_transpiled(
            "SELECT DATE_TRUNC('YEAR', '2015-03-05T09:32:05.359')",
            write={
                "databricks": "SELECT date_trunc('YEAR', '2015-03-05T09:32:05.359');",
            },
        )
        # Test case to validate `date_trunc` conversion of column
        self.validate_all_transpiled(
            "SELECT DATE_TRUNC('MONTH', col1) AS date_trunc_col1 FROM tabl",
            write={
                "databricks": "SELECT date_trunc('MM', col1) AS date_trunc_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `date_trunc` conversion error:
            # UNIT is a mandatory argument: `date_trunc(unit, expr)`
            self.validate_all_transpiled(
                "SELECT DATE_TRUNC(col1) AS date_trunc_col1 FROM tabl",
                write={
                    "databricks": "SELECT date_trunc(col1) AS date_trunc_col1 FROM tabl;",
                },
            )

    def test_iff(self):
        # Test case to validate `iff` conversion of column
        self.validate_all_transpiled(
            "SELECT IF(cond, col1, col2) AS iff_col1 FROM tabl",
            write={
                "databricks": "SELECT iff(cond, col1, col2) AS iff_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `iff` conversion of column:
            # three arguments are needed (iff(cond, expr1, expr2)
            self.validate_all_transpiled(
                "SELECT IFF(col1) AS iff_col1 FROM tabl",
                write={
                    "databricks": "SELECT iff(col1) AS iff_col1 FROM tabl;",
                },
            )

    def test_lower(self):
        # Test case to validate `lower` conversion of column
        self.validate_all_transpiled(
            "SELECT LOWER(col1) AS lower_col1 FROM tabl",
            write={
                "databricks": "SELECT lower(col1) AS lower_col1 FROM tabl;",
            },
        )

    def test_avg(self):
        # Test case to validate `avg` conversion of column
        self.validate_all_transpiled(
            "SELECT AVG(col1) AS avg_col1 FROM tabl",
            write={
                "databricks": "SELECT avg(col1) AS avg_col1 FROM tabl;",
            },
        )

    def test_ifnull(self):
        # Test case to validate `ifnull` conversion of column with two expressions
        self.validate_all_transpiled(
            "SELECT COALESCE(col1, 'NA') AS ifnull_col1 FROM tabl",
            write={
                "databricks": "SELECT ifnull(col1, 'NA') AS ifnull_col1 FROM tabl;",
            },
        )
        # Test case to validate `ifnull` conversion of single column:
        self.validate_all_transpiled(
            "SELECT COALESCE(col1) AS ifnull_col1 FROM tabl",
            write={
                "databricks": "SELECT ifnull(col1) AS ifnull_col1 FROM tabl;",
            },
        )

    def test_current_date(self):
        # Test case to validate `current_date` conversion of column
        self.validate_all_transpiled(
            "SELECT CURRENT_DATE FROM tabl",
            write={
                "databricks": "SELECT current_date() FROM tabl;",
            },
        )

    # [TODO]
    # Date or time parts used in Snowflake differ from the ones used in Databricks. Need to handle this case.
    def test_extract(self):
        # Test case to validate `extract` conversion of column
        self.validate_all_transpiled(
            "SELECT EXTRACT(week FROM col1) AS extract_col1 FROM tabl",
            write={
                "databricks": "SELECT extract(week FROM col1) AS extract_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `extract` conversion of column: ParseError
            # field and source are needed: `extract(field FROM source)`
            self.validate_all_transpiled(
                "SELECT EXTRACT(col1) AS extract_col1 FROM tabl",
                write={
                    "databricks": "SELECT extract(col1) AS extract_col1 FROM tabl;",
                },
            )

    # [TODO]
    # Snowflake can take an optional time precision argument. Need to handle this case in Databricks.
    def test_current_timestamp(self):
        # Test case to validate `current_timestamp` conversion of column
        self.validate_all_transpiled(
            "SELECT CURRENT_TIMESTAMP() AS current_timestamp_col1 FROM tabl",
            write={
                "databricks": "SELECT current_timestamp(col1) AS current_timestamp_col1 FROM tabl;",
            },
        )

    def test_any_value(self):
        # Test case to validate `any_value` conversion of column
        self.validate_all_transpiled(
            "SELECT customer.id, ANY_VALUE(customer.name), SUM(orders.value) FROM customer JOIN orders ON customer.id "
            "= orders.customer_id GROUP BY customer.id",
            write={
                "databricks": "SELECT customer.id , ANY_VALUE(customer.name) , SUM(orders.value) FROM customer JOIN "
                "orders ON customer.id = orders.customer_id GROUP BY customer.id;",
            },
        )

    def test_abs(self):
        # Test case to validate `abs` conversion of column
        self.validate_all_transpiled(
            "SELECT ABS(col1) AS abs_col1 FROM tabl",
            write={
                "databricks": "SELECT abs(col1) AS abs_col1 FROM tabl;",
            },
        )

    # [TODO]
    # In Snowflake, this function is overloaded; it can also be used as a numeric function to round down numeric
    # expressions. Also, it can take data time parts which are not supported in Databricks TRUNC function.
    # It may be transpiled to DATE_TRUNK function in Databric

    def test_lag(self):
        # Test case to validate `lag` conversion of column
        self.validate_all_transpiled(
            "SELECT LAG(col1) AS lag_col1 FROM tabl",
            write={
                "databricks": "SELECT lag(col1) AS lag_col1 FROM tabl;",
            },
        )

    # [TODO]
    # In Snowflake replacement argument is optional and the default is an empty string
    # Also, occurrence and parameters arguments are not supported in Databricks
    # Need to handle these cases.

    def test_greatest(self):
        # Test case to validate `greatest` conversion of column
        self.validate_all_transpiled(
            "SELECT GREATEST(col_1, col_2, col_3) AS greatest_col1 FROM tabl",
            write={
                "databricks": "SELECT greatest(col_1, col_2, col_3) AS greatest_col1 FROM tabl;",
            },
        )

    def test_floor(self):
        # Test case to validate `floor` conversion of column
        self.validate_all_transpiled(
            "SELECT FLOOR(col1) AS floor_col1 FROM tabl",
            write={
                "databricks": "SELECT floor(col1) AS floor_col1 FROM tabl;",
            },
        )

    def test_least(self):
        # Test case to validate `least` conversion of column
        self.validate_all_transpiled(
            "SELECT LEAST(col1) AS least_col1 FROM tabl",
            write={
                "databricks": "SELECT least(col1) AS least_col1 FROM tabl;",
            },
        )

    # [TODO]
    # DATE_PART in Snowflake can take various field names. Need to handle these cases.
    def test_date_part(self):
        # Test case to validate `date_part` conversion of column
        self.validate_all_transpiled(
            "SELECT EXTRACT(second FROM col1) AS date_part_col1 FROM tabl",
            write={
                "databricks": "SELECT date_part('seconds', col1) AS date_part_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `date_part` conversion of column: ParseError
            # fieldStr, expr are mandatory: `date_part(fieldStr, expr)`
            self.validate_all_transpiled(
                "SELECT DATE_PART(col1) AS date_part_col1 FROM tabl",
                write={
                    "databricks": "SELECT date_part(col1) AS date_part_col1 FROM tabl;",
                },
            )

    # [TODO]
    # Databricks doesn't take the optional date_part argument. Handle the case.
    def test_last_day(self):
        # Test case to validate `last_day` conversion of column
        self.validate_all_transpiled(
            "SELECT LAST_DAY(col1) AS last_day_col1 FROM tabl",
            write={
                "databricks": "SELECT last_day(col1) AS last_day_col1 FROM tabl;",
            },
        )

    # [TODO]
    # flatten in Snowflake doesn't have a direct counterpart in Databricks.
    # The returned rows in flatten consist of a fixed set of columns:
    # +-----+------+------+-------+-------+------+
    # | SEQ |  KEY | PATH | INDEX | VALUE | THIS |
    # |-----+------+------+-------+-------+------|
    # Explode does not have this columns.
    # The closest function in Databricks is `posexplode`
    # This case needs to be handled. May be with a warning message?
    def test_flatten(self):
        # Test case to validate `flatten` conversion of column
        self.validate_all_transpiled(
            "SELECT EXPLODE(col1) AS flatten_col1 FROM tabl",
            write={
                "databricks": "SELECT flatten(col1) AS flatten_col1 FROM tabl;",
            },
        )

    def test_left(self):
        # Test case to validate `left` conversion of column
        self.validate_all_transpiled(
            "SELECT LEFT(col1, 3) AS left_col1 FROM tabl",
            write={
                "databricks": "SELECT left(col1, 3) AS left_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `left` conversion of column: ParseError
            # str, len both are needed: `left(str, len)`
            self.validate_all_transpiled(
                "SELECT LEFT(col1) AS left_col1 FROM tabl",
                write={
                    "databricks": "SELECT left(col1) AS left_col1 FROM tabl;",
                },
            )

    def test_lead(self):
        # Test case to validate `lead` conversion of column
        self.validate_all_transpiled(
            "SELECT LEAD(col1) AS lead_col1 FROM tabl",
            write={
                "databricks": "SELECT lead(col1) AS lead_col1 FROM tabl;",
            },
        )

    # [TODO]
    # The separator argument in Snowflake is a plain string. But in Databricks it is a regex
    # For example, in Snowflake, we can call SPLIT('127.0.0.1', '.') but in Databricks we need to call
    # SPLIT('127.0.0.1', '\\.')
    # Need to handle this case.
    #
    # def test_split(self):
    #     # Test case to validate `split` conversion of column
    #     self.validate_all_transpiled(
    #         "SELECT SPLIT(col1, '[|.]') AS split_col1 FROM tabl",
    #         write={
    #             "databricks": "SELECT split(col1, '[|.]') AS split_col1 FROM tabl;",
    #         },
    #     )
    #     with self.assertRaises(ParseError):
    #         # Test case to validate `split` conversion of column: ParseError
    #         # str, regexp are mandatory. limit is Optional: `split(str, regex [, limit] )`
    #         self.validate_all_transpiled(
    #             "SELECT SPLIT(col1) AS split_col1 FROM tabl",
    #             write={
    #                 "databricks": "SELECT split(col1) AS split_col1 FROM tabl;",
    #             },
    #         )

    def test_contains(self):
        # Test case to validate `contains` conversion of column
        self.validate_all_transpiled(
            "SELECT CONTAINS('SparkSQL', 'Spark')",
            write={
                "databricks": "SELECT contains('SparkSQL', 'Spark');",
            },
        )

    def test_last_value(self):
        # Test case to validate `last_value` conversion of column
        self.validate_all_transpiled(
            "SELECT LAST_VALUE(col1) AS last_value_col1 FROM tabl",
            write={
                "databricks": "SELECT last_value(col1) AS last_value_col1 FROM tabl;",
            },
        )

    def test_lpad(self):
        # Test case to validate `lpad` conversion of column
        self.validate_all_transpiled(
            "SELECT LPAD('hi', 5, 'ab')",
            write={
                "databricks": "SELECT lpad('hi', 5, 'ab');",
            },
        )

    def test_equal_null(self):
        # Test case to validate `equal_null` conversion of column
        self.validate_all_transpiled(
            "SELECT EQUAL_NULL(2, 2) AS equal_null_col1 FROM tabl",
            write={
                "databricks": "SELECT equal_null(2, 2) AS equal_null_col1 FROM tabl;",
            },
        )

    # [TODO]
    # Both Databricks and Snowflake can take an optional set of characters to be trimmed as parameter.
    # Need to handle that case.
    def test_ltrim(self):
        # Test case to validate `ltrim` conversion of column
        self.validate_all_transpiled(
            "SELECT LTRIM(col1) AS ltrim_col1 FROM tabl",
            write={
                "databricks": "SELECT ltrim(col1) AS ltrim_col1 FROM tabl;",
            },
        )

    def test_array_size(self):
        # Test case to validate `array_size` conversion of column
        self.validate_all_transpiled(
            "SELECT SIZE(col1) AS array_size_col1 FROM tabl",
            write={
                "databricks": "SELECT array_size(col1) AS array_size_col1 FROM tabl;",
            },
        )

    def test_first_value(self):
        # Test case to validate `first_value` conversion of column
        self.validate_all_transpiled(
            "SELECT FIRST_VALUE(col1) AS first_value_col1 FROM tabl",
            write={
                "databricks": "SELECT first_value(col1) AS first_value_col1 FROM tabl;",
            },
        )

    def test_median(self):
        # Test case to validate `median` conversion of column
        self.validate_all_transpiled(
            "SELECT MEDIAN(col1) AS median_col1 FROM tabl",
            write={
                "databricks": "SELECT median(col1) AS median_col1 FROM tabl;",
            },
        )

    def test_get(self):
        # Test case to validate `get` conversion of column
        self.validate_all_transpiled(
            "SELECT GET(col1) AS get_col1 FROM tabl",
            write={
                "databricks": "SELECT get(col1) AS get_col1 FROM tabl;",
            },
        )

    def test_add_months(self):
        # Test case to validate `add_months` conversion of column
        self.validate_all_transpiled(
            "SELECT ADD_MONTHS(col1) AS add_months_col1 FROM tabl",
            write={
                "databricks": "SELECT add_months(col1) AS add_months_col1 FROM tabl;",
            },
        )

    def test_array_contains(self):
        # Test case to validate `array_contains` conversion of column
        # The order of arguments is different in Databricks and Snowflake
        self.validate_all_transpiled(
            "SELECT ARRAY_CONTAINS(arr_col, 33) AS array_contains_col1 FROM tabl",
            write={
                "databricks": "SELECT array_contains(33, arr_col) AS array_contains_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `array_contains` conversion of column
            # array, value both are mandatory args: `array_contains(array, value)`
            self.validate_all_transpiled(
                "SELECT ARRAY_CONTAINS(arr_col) AS array_contains_col1 FROM tabl",
                write={
                    "databricks": "SELECT array_contains(arr_col) AS array_contains_col1 FROM tabl;",
                },
            )

    def test_hash(self):
        # Test case to validate `hash` conversion of column
        self.validate_all_transpiled(
            "SELECT HASH(col1) AS hash_col1 FROM tabl",
            write={
                "databricks": "SELECT hash(col1) AS hash_col1 FROM tabl;",
            },
        )

    def test_arrays_overlap(self):
        # Test case to validate `arrays_overlap` conversion of column
        self.validate_all_transpiled(
            "SELECT ARRAYS_OVERLAP(ARRAY(1, 2, NULL), ARRAY(3, NULL, 5))",
            write={
                "databricks": "SELECT ARRAYS_OVERLAP(ARRAY_CONSTRUCT(1, 2, NULL), ARRAY_CONSTRUCT(3, NULL, 5));",
            },
        )

    def test_dense_rank(self):
        # Test case to validate `dense_rank` conversion of column
        self.validate_all_transpiled(
            "SELECT DENSE_RANK(col1) AS dense_rank_col1 FROM tabl",
            write={
                "databricks": "SELECT dense_rank(col1) AS dense_rank_col1 FROM tabl;",
            },
        )

    # [TODO]
    # Snowflake can also take an optional argument delimiters.
    # Need to handle that, may be add a warning message if delimiter is present
    def test_initcap(self):
        # Test case to validate `initcap` conversion of column
        self.validate_all_transpiled(
            "SELECT INITCAP(col1) AS initcap_col1 FROM tabl",
            write={
                "databricks": "SELECT initcap(col1) AS initcap_col1 FROM tabl;",
            },
        )

    def test_count_if(self):
        # Test case to validate `count_if` conversion of column
        self.validate_all_transpiled(
            "SELECT COUNT_IF(j_col > i_col) FROM basic_example",
            write={
                "databricks": "SELECT COUNT_IF(j_col > i_col) FROM basic_example;",
            },
        )

    def test_ceil(self):
        # Test case to validate `ceil` conversion of column
        self.validate_all_transpiled(
            "SELECT CEIL(col1) AS ceil_col1 FROM tabl",
            write={
                "databricks": "SELECT ceil(col1) AS ceil_col1 FROM tabl;",
            },
        )

    # [TODO]
    # Currently the transpiler converts the decode function to CASE.
    # Databricks has native decode function which behaves like the same function in Snowflake.
    # We can use that instead.
    def test_decode(self):
        # Test case to validate `decode` conversion of column
        self.validate_all_transpiled(
            "SELECT CASE WHEN column1 = 1 THEN 'one' WHEN column1 = 2 THEN 'two' WHEN column1 IS NULL THEN '-NULL-' "
            "ELSE 'other' END AS decode_result",
            write={
                "databricks": "SELECT decode(column1, 1, 'one', 2, 'two', NULL, '-NULL-', 'other') AS decode_result;",
            },
        )

    def test_exp(self):
        # Test case to validate `exp` conversion of column
        self.validate_all_transpiled(
            "SELECT EXP(col1) AS exp_col1 FROM tabl",
            write={
                "databricks": "SELECT exp(col1) AS exp_col1 FROM tabl;",
            },
        )

    def test_cos(self):
        # Test case to validate `cos` conversion of column
        self.validate_all_transpiled(
            "SELECT COS(col1) AS cos_col1 FROM tabl",
            write={
                "databricks": "SELECT cos(col1) AS cos_col1 FROM tabl;",
            },
        )

    def test_endswith(self):
        # Test case to validate `endswith` conversion of column
        self.validate_all_transpiled(
            "SELECT ENDSWITH('SparkSQL', 'SQL')",
            write={
                "databricks": "SELECT endswith('SparkSQL', 'SQL');",
            },
        )

    def test_concat_ws(self):
        # Test case to validate `concat_ws` conversion of column
        self.validate_all_transpiled(
            "SELECT CONCAT_WS(',', 'one', 'two', 'three')",
            write={
                "databricks": "SELECT CONCAT_WS(',', 'one', 'two', 'three');",
            },
        )

    def test_array_prepend(self):
        # Test case to validate `array_prepend` conversion of column
        self.validate_all_transpiled(
            "SELECT ARRAY_PREPEND(array, elem) AS array_prepend_col1 FROM tabl",
            write={
                "databricks": "SELECT array_prepend(array, elem) AS array_prepend_col1 FROM tabl;",
            },
        )

    def test_log(self):
        # Test case to validate `log` conversion of column
        self.validate_all_transpiled(
            "SELECT LOG(x, y) AS log_col1 FROM tabl",
            write={
                "databricks": "SELECT log(x, y) AS log_col1 FROM tabl;",
            },
        )

    def test_approx_percentile(self):
        # Test case to validate `approx_percentile` conversion of column
        self.validate_all_transpiled(
            "SELECT APPROX_PERCENTILE(col1, 0.5) AS approx_percentile_col1 FROM tabl",
            write={
                "databricks": "SELECT approx_percentile(col1, 0.5) AS approx_percentile_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `approx_percentile` conversion of column: ParseError
            # expr, percentile are mandatory. accuracy, cond are optional
            # `approx_percentile ( [ALL | DISTINCT] expr, percentile [, accuracy] ) [ FILTER ( WHERE cond ) ]`
            self.validate_all_transpiled(
                "SELECT APPROX_PERCENTILE(col1) AS approx_percentile_col1 FROM tabl",
                write={
                    "databricks": "SELECT approx_percentile(col1) AS approx_percentile_col1 FROM tabl;",
                },
            )

    def test_array_distinct(self):
        # Test case to validate `array_distinct` conversion of column
        self.validate_all_transpiled(
            "SELECT ARRAY_DISTINCT(col1) AS array_distinct_col1 FROM tabl",
            write={
                "databricks": "SELECT array_distinct(col1) AS array_distinct_col1 FROM tabl;",
            },
        )

    def test_array_compact(self):
        # Test case to validate `array_compact` conversion of column
        self.validate_all_transpiled(
            "SELECT ARRAY_COMPACT(col1) AS array_compact_col1 FROM tabl",
            write={
                "databricks": "SELECT array_compact(col1) AS array_compact_col1 FROM tabl;",
            },
        )

    def test_corr(self):
        # Test case to validate `corr` conversion of column
        self.validate_all_transpiled(
            "SELECT CORR(v, v2) AS corr_col1 FROM tabl",
            write={
                "databricks": "SELECT CORR(v, v2) AS corr_col1 FROM tabl;",
            },
        )

    def test_asin(self):
        # Test case to validate `asin` conversion of column
        self.validate_all_transpiled(
            "SELECT ASIN(col1) AS asin_col1 FROM tabl",
            write={
                "databricks": "SELECT asin(col1) AS asin_col1 FROM tabl;",
            },
        )

    # [TODO]
    # Default argument values are different in Snowflake and Databricks
    # Need to handle these cases.
    def test_approx_top_k(self):
        # Test case to validate `approx_top_k` conversion of column
        self.validate_all_transpiled(
            "SELECT APPROX_TOP_K(col1) AS approx_top_k_col1 FROM tabl",
            write={
                "databricks": "SELECT approx_top_k(col1) AS approx_top_k_col1 FROM tabl;",
            },
        )

    def test_cume_dist(self):
        # Test case to validate `cume_dist` conversion of column
        self.validate_all_transpiled(
            "SELECT CUME_DIST() AS cume_dist_col1 FROM tabl",
            write={
                "databricks": "SELECT cume_dist() AS cume_dist_col1 FROM tabl;",
            },
        )

    def test_array_except(self):
        # Test case to validate `array_except` conversion of column
        self.validate_all_transpiled(
            "SELECT ARRAY_EXCEPT(a, b) AS array_except_col1 FROM tabl",
            write={
                "databricks": "SELECT array_except(a, b) AS array_except_col1 FROM tabl;",
            },
        )

    def test_current_database(self):
        # Test case to validate `current_database` conversion of column
        self.validate_all_transpiled(
            "SELECT CURRENT_DATABASE() AS current_database_col1 FROM tabl",
            write={
                "databricks": "SELECT current_database() AS current_database_col1 FROM tabl;",
            },
        )

    def test_array_append(self):
        # Test case to validate `array_append` conversion of column
        self.validate_all_transpiled(
            "SELECT ARRAY_APPEND(array, elem) AS array_append_col1 FROM tabl",
            write={
                "databricks": "SELECT array_append(array, elem) AS array_append_col1 FROM tabl;",
            },
        )

    # [TODO]
    # In Snowflake and Databricks the positions of the arguments are interchanged.
    # Needs to be handled in the transpiler.
    def test_array_position(self):
        # Test case to validate `array_position` conversion of column
        self.validate_all_transpiled(
            "SELECT ARRAY_POSITION(col1) AS array_position_col1 FROM tabl",
            write={
                "databricks": "SELECT array_position(col1) AS array_position_col1 FROM tabl;",
            },
        )

    def test_array_remove(self):
        # Test case to validate `array_remove` conversion of column
        self.validate_all_transpiled(
            "SELECT ARRAY_REMOVE(array, element) AS array_remove_col1 FROM tabl",
            write={
                "databricks": "SELECT array_remove(array, element) AS array_remove_col1 FROM tabl;",
            },
        )

    def test_atan2(self):
        # Test case to validate `atan2` conversion of column
        self.validate_all_transpiled(
            "SELECT ATAN2(exprY, exprX) AS atan2_col1 FROM tabl",
            write={
                "databricks": "SELECT atan2(exprY, exprX) AS atan2_col1 FROM tabl;",
            },
        )

    def test_dayname(self):
        # Test case to validate `dayname` parsing of timestamp column
        self.validate_all_transpiled(
            """SELECT DATE_FORMAT(TO_TIMESTAMP('2015-04-03 10:00:00', 'yyyy-MM-dd HH:mm:ss'), 'E') AS MONTH""",
            write={
                "databricks": """SELECT DAYNAME(TO_TIMESTAMP('2015-04-03 10:00:00')) AS MONTH;""",
            },
        )
        # Test case to validate `dayname` parsing of date column
        self.validate_all_transpiled(
            """SELECT DATE_FORMAT(TO_DATE('2015-05-01'), 'E') AS MONTH""",
            write={
                "databricks": """SELECT DAYNAME(TO_DATE('2015-05-01')) AS MONTH;""",
            },
        )
        # Test case to validate `dayname` parsing of string column with hours and minutes
        self.validate_all_transpiled(
            """SELECT DATE_FORMAT('2015-04-03 10:00', 'E') AS MONTH""",
            write={
                "databricks": """SELECT DAYNAME('2015-04-03 10:00') AS MONTH;""",
            },
        )

    def test_booland_agg(self):
        self.validate_all_transpiled(
            "SELECT BOOL_AND(k) FROM bool_example",
            write={
                "databricks": "select booland_agg(k) from bool_example",
            },
        )
        self.validate_all_transpiled(
            "SELECT s2, BOOL_AND(k) FROM bool_example GROUP BY s2",
            write={
                "databricks": "select s2, booland_agg(k) from bool_example group by s2",
            },
        )

    def test_base64_encode(self):
        self.validate_all_transpiled(
            "SELECT BASE64('HELLO'), BASE64('HELLO')",
            write={
                "databricks": "SELECT BASE64_ENCODE('HELLO'), BASE64_ENCODE('HELLO');",
            },
        )

    def test_base64_decode(self):
        self.validate_all_transpiled(
            "SELECT UNBASE64(BASE64('HELLO')), UNBASE64(BASE64('HELLO'))",
            write={
                "databricks": "SELECT BASE64_DECODE_STRING(BASE64_ENCODE('HELLO')), "
                "TRY_BASE64_DECODE_STRING(BASE64_ENCODE('HELLO'));",
            },
        )

    def test_array_compact_construct(self):
        self.validate_all_transpiled(
            "SELECT ARRAY(NULL, 'hello', CAST(3 AS DOUBLE), 4, 5)",
            write={
                "databricks": "SELECT ARRAY_CONSTRUCT(null, 'hello', 3::double, 4, 5);",
            },
        )
        self.validate_all_transpiled(
            "SELECT ARRAY_EXCEPT(ARRAY(NULL, 'hello', CAST(3 AS DOUBLE), 4, 5), ARRAY(NULL))",
            write={
                "databricks": "SELECT ARRAY_CONSTRUCT_COMPACT(null, 'hello', 3::double, 4, 5);",
            },
        )

    def test_array_intersection(self):
        self.validate_all_transpiled(
            "SELECT ARRAY_INTERSECT(col1, col2)",
            write={
                "databricks": "SELECT ARRAY_INTERSECTION(col1, col2)",
            },
        )
        self.validate_all_transpiled(
            "SELECT ARRAY_INTERSECT(ARRAY(1, 2, 3), ARRAY(1, 2))",
            write={
                "databricks": "SELECT ARRAY_INTERSECTION(ARRAY_CONSTRUCT(1, 2, 3), ARRAY_CONSTRUCT(1, 2))",
            },
        )

    def test_array_slice(self):
        # Test Case to validate SF ARRAY_SLICE conversion to SLICE in Databricks
        self.validate_all_transpiled(
            "SELECT SLICE(ARRAY(0, 1, 2, 3, 4, 5, 6), 1, 2)",
            write={
                "databricks": "SELECT array_slice(array_construct(0,1,2,3,4,5,6), 0, 2);",
            },
        )
        # Test Case to validate SF ARRAY_SLICE conversion to SLICE in Databricks with negative `from`
        self.validate_all_transpiled(
            "SELECT SLICE(ARRAY(90, 91, 92, 93, 94, 95, 96), -5, 3)",
            write={
                "databricks": "SELECT array_slice(array_construct(90,91,92,93,94,95,96), -5, 3);",
            },
        )
        with self.assertRaises(UnsupportedError):
            # Test Case to validate SF ARRAY_SLICE conversion to SLICE in Databricks with negative `to`
            # In Databricks: function `slice` length must be greater than or equal to 0
            self.validate_all_transpiled(
                "SELECT SLICE(ARRAY(90, 91, 92, 93, 94, 95, 96), -4, -1)",
                write={
                    "databricks": "SELECT array_slice(array_construct(90,91,92,93,94,95,96), -4, -1);",
                },
            )

    def test_json_extract_path_text(self):
        self.validate_all_transpiled(
            "SELECT GET_JSON_OBJECT(json_data, '$.level_1_key.level_2_key[1]') FROM demo1",
            write={
                "databricks": "SELECT JSON_EXTRACT_PATH_TEXT(json_data, 'level_1_key.level_2_key[1]') FROM demo1;",
            },
        )

        self.validate_all_transpiled(
            "SELECT GET_JSON_OBJECT(json_data, CONCAT('$.', path_col)) FROM demo1",
            write={
                "databricks": "SELECT JSON_EXTRACT_PATH_TEXT(json_data, path_col) FROM demo1;",
            },
        )

        self.validate_all_transpiled(
            "SELECT GET_JSON_OBJECT('{}', CONCAT('$.', path_col)) FROM demo1",
            write={
                "databricks": "SELECT JSON_EXTRACT_PATH_TEXT('{}', path_col) FROM demo1;",
            },
        )
