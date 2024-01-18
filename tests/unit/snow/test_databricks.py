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

    def test_struct(self):
        # Test case to validate JSON to STRUCT conversion
        self.validate_all_transpiled(
            """SELECT STRUCT(1 AS a, 2 AS b), ARRAY(STRUCT(11 AS C, 22 AS d), 3)""",
            write={
                "databricks": """SELECT {'a': 1, 'b': 2}, [{'c': 11, 'd': 22}, 3];""",
            },
        )

    def test_lateral_struct(self):
        self.validate_all_transpiled(
            """SELECT p.value.id AS `ID` FROM persons_struct AS p""",
            write={
                "databricks": """SELECT p.value:id as "ID" FROM persons_struct p;""",
            },
        )
        self.validate_all_transpiled(
            """SELECT f.name AS `Contact`,
                          f.first,
                          CAST(p.value.id AS DOUBLE) AS `id_parsed`,
                          p.c.value.first,
                          p.value
                   FROM persons_struct AS p\n LATERAL VIEW EXPLODE($p.$c.contact) AS f""",
            write={
                "databricks": """SELECT f.value:name AS "Contact",
                                        f.value:first,
                                        p.value:id::FLOAT AS "id_parsed",
                                        p.c:value:first,
                                        p.value
                                 FROM persons_struct p, lateral flatten(input => ${p}.${c}, path => 'contact') f;""",
            },
        )
        self.validate_all_transpiled(
            """SELECT CAST(d.value.display_position AS DECIMAL(38, 0)) AS item_card_impression_display_position,
                          CAST(i.impression_attributes AS STRING) AS item_card_impression_impression_attributes,
                          CAST(CURRENT_TIMESTAMP() AS TIMESTAMP) AS dwh_created_date_time_utc,
                          CAST(i.propensity AS DOUBLE) AS propensity, candidates
                   FROM dwh.vw_replacement_customer AS d\n LATERAL VIEW OUTER EXPLODE(d.item_card_impressions) AS i
                   WHERE event_date_pt = '{start_date}' AND event_name IN ('store.replacements_view')""",
            write={
                "databricks": """SELECT d.value:display_position::NUMBER as item_card_impression_display_position,
                                   i.value:impression_attributes::VARCHAR as item_card_impression_impression_attributes,
                                   cast(current_timestamp() as timestamp_ntz(9)) as dwh_created_date_time_utc,
                                   i.value:propensity::FLOAT as propensity,
                                   candidates
                                 FROM dwh.vw_replacement_customer  d,
                                 LATERAL FLATTEN (INPUT => d.item_card_impressions, OUTER => TRUE) i
                                 WHERE event_date_pt = '{start_date}' and event_name in ('store.replacements_view')""",
            },
        )
        self.validate_all_transpiled(
            """SELECT tt.id AS tax_transaction_id,
                          CAST(tt.response_body.isMpfState AS BOOLEAN) AS is_mpf_state,
                          REGEXP_REPLACE(tt.request_body.deliveryLocation.city, '""', '') AS delivery_city,
                          REGEXP_REPLACE(tt.request_body.store.storeAddress.zipCode, '""', '') AS store_zipcode
                   FROM tax_table AS tt""",
            write={
                "databricks": """SELECT
                                   tt.id AS tax_transaction_id,
                                   cast(tt.response_body:"isMpfState" AS BOOLEAN) AS is_mpf_state,
                                   REGEXP_REPLACE(tt.request_body:"deliveryLocation":"city", '""', '') AS delivery_city,
                                   REGEXP_REPLACE(tt.request_body:"store":"storeAddress":"zipCode", '""', '') AS
                                   store_zipcode
                                   FROM tax_table  tt
                              """,
            },
        )
        self.validate_all_transpiled(
            """SELECT varchar1, CAST(float1 AS STRING), CAST(variant1.`Loan Number` AS STRING) FROM tmp""",
            write={
                "databricks": """ select varchar1,
                                        float1::varchar,
                                        variant1:"Loan Number"::varchar from tmp;
                              """,
            },
        )
        self.validate_all_transpiled(
            """SELECT ARRAY_EXCEPT(ARRAY(STRUCT(1 AS a, 2 AS b), 1), ARRAY(STRUCT(1 AS a, 2 AS b), 3))""",
            write={
                "databricks": """SELECT ARRAY_EXCEPT([{'a': 1, 'b': 2}, 1], [{'a': 1, 'b': 2}, 3]);""",
            },
        )
        self.validate_all_transpiled(
            """SELECT v, v.food, TO_JSON(v) FROM jdemo1""",
            write={
                "databricks": """SELECT v, v:food, TO_JSON(v) FROM jdemo1;""",
            },
        )
        self.validate_all_transpiled(
            """SELECT STRIP_NULL_VALUE(src.c) FROM mytable""",
            write={
                "databricks": """SELECT STRIP_NULL_VALUE(src:c) FROM mytable;""",
            },
        )
        self.validate_all_transpiled(
            """SELECT CAST(los.objectDomain AS STRING) AS object_type,
                          CAST(los.objectName AS STRING) AS object_name,
                          CAST(cols.columnName AS STRING) AS column_name,
                          COUNT(DISTINCT lah.query_token) AS n_queries,
                          COUNT(DISTINCT lah.consumer_account_locator) AS n_distinct_consumer_accounts
                   FROM SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY AS lah
                   LATERAL VIEW EXPLODE(lah.listing_objects_accessed) AS los
                   LATERAL VIEW EXPLODE(los.value.columns) AS cols
                   WHERE TRUE AND CAST(los.value.objectDomain AS STRING) IN ('Table', 'View') AND
                        query_date BETWEEN '2022-03-01' AND '2022-04-30' AND
                        CAST(los.value.objectName AS STRING) = 'DATABASE_NAME.SCHEMA_NAME.TABLE_NAME' AND
                        lah.consumer_account_locator = 'CONSUMER_ACCOUNT_LOCATOR' GROUP BY 1, 2, 3""",
            write={
                "databricks": """select
                                      los.value:"objectDomain"::string as object_type,
                                      los.value:"objectName"::string as object_name,
                                      cols.value:"columnName"::string as column_name,
                                      count(distinct lah.query_token) as n_queries,
                                      count(distinct lah.consumer_account_locator) as n_distinct_consumer_accounts
                                 from SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY as lah
                                 join lateral flatten(input=>lah.listing_objects_accessed) as los
                                 join lateral flatten(input=>los.value, path=>'columns') as cols
                                 where true
                                      and los.value:"objectDomain"::string in ('Table', 'View')
                                      and query_date between '2022-03-01' and '2022-04-30'
                                      and los.value:"objectName"::string = 'DATABASE_NAME.SCHEMA_NAME.TABLE_NAME'
                                      and lah.consumer_account_locator = 'CONSUMER_ACCOUNT_LOCATOR'
                                    group by 1,2,3;
                                """,
            },
        )
        self.validate_all_transpiled(
            """SELECT tt.id, FROM_JSON(tt.details, {TT.DETAILS_SCHEMA}) FROM prod.public.table AS tt
                 LATERAL VIEW EXPLODE(FROM_JSON(FROM_JSON(tt.resp)['items'])) AS lit
                 LATERAL VIEW EXPLODE(FROM_JSON(lit.value['details'])) AS ltd""",
            write={
                "databricks": """
                SELECT
                tt.id
                , PARSE_JSON(tt.details)
                FROM prod.public.table tt
                ,  LATERAL FLATTEN (input=> PARSE_JSON(PARSE_JSON(tt.resp):items)) AS lit
                ,  LATERAL FLATTEN (input=> parse_json(lit.value:"details")) AS ltd;""",
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

    def test_strtok_to_array(self):
        # Test case to validate the static String and default delimiter
        self.validate_all_transpiled(
            """SELECT SPLIT('my text is divided','[ ]')""",
            write={
                "databricks": """select STRTOK_TO_ARRAY('my text is divided');""",
            },
        )
        # Test case to validate the conversion of static String and table column with delimiter
        self.validate_all_transpiled(
            """SELECT SPLIT('v_p_n','[_]'), SPLIT(col123,'[.]') FROM table AS tbl""",
            write={
                "databricks": """select STRTOK_TO_ARRAY('v_p_n', "_"), STRTOK_TO_ARRAY(col123, ".") FROM table tbl;""",
            },
        )
        # Test case to validate the static String and delimiter
        self.validate_all_transpiled(
            """SELECT SPLIT('a@b.c','[.@]')""",
            write={
                "databricks": """select STRTOK_TO_ARRAY('a@b.c', ".@");""",
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
        self.validate_all_transpiled(
            """SELECT MAKE_DATE(2023, 10, 3), MAKE_DATE(2020, 4, 4)""",
            write={
                "databricks": """select datefromparts(2023, 10, 3), datefromparts(2020, 4, 4);""",
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

    def test_try_to_date(self):
        # Test case to validate `TRY_TO_DATE` parsing with default format
        self.validate_all_transpiled(
            """SELECT DATE(TRY_TO_TIMESTAMP('2018-05-15', 'yyyy-MM-dd'))""",
            write={
                "databricks": """SELECT TRY_TO_DATE('2018-05-15')""",
            },
        )
        # Test case to validate `TRY_TO_DATE` parsing with custom format
        self.validate_all_transpiled(
            """SELECT DATE(TRY_TO_TIMESTAMP('2023-25-09', 'yyyy-dd-MM'))""",
            write={
                "databricks": """SELECT TRY_TO_DATE('2023-25-09', 'yyyy-dd-MM')""",
            },
        )
        # Test case to validate `TRY_TO_DATE` String, column parsing with custom format
        self.validate_all_transpiled(
            """SELECT DATE(TRY_TO_TIMESTAMP('2012.20.12', 'yyyy.dd.MM')),
            DATE(TRY_TO_TIMESTAMP(d.col1, 'yyyy-MM-dd')) FROM dummy AS d""",
            write={
                "databricks": """SELECT TRY_TO_DATE('2012.20.12', 'yyyy.dd.MM'), TRY_TO_DATE(d.col1) FROM dummy d""",
            },
        )

    def test_try_to_timestamp(self):
        # Test case to validate `TRY_TO_TIMESTAMP` parsing
        self.validate_all_transpiled(
            """SELECT TRY_TO_TIMESTAMP('2016-12-31 00:12:00')""",
            write={
                "databricks": """SELECT TRY_TO_TIMESTAMP('2016-12-31 00:12:00')""",
            },
        )
        # Test case to validate `TRY_TO_TIMESTAMP` String, column parsing with custom format
        self.validate_all_transpiled(
            """SELECT TRY_TO_TIMESTAMP('2018-05-15', 'yyyy-MM-dd')""",
            write={
                "databricks": """SELECT TRY_TO_TIMESTAMP('2018-05-15', 'yyyy-MM-dd')""",
            },
        )

    def test_strtok(self):
        # Test case to validate the static String, default delimiter (single space) and default partition number (1)
        self.validate_all_transpiled(
            """SELECT SPLIT_PART('my text is divided', ' ', 1)""",
            write={
                "databricks": """select STRTOK('my text is divided');""",
            },
        )
        # Test case to validate the static String, table column, delimiter and partition number
        self.validate_all_transpiled(
            """SELECT SPLIT_PART('a_b_c', ' ', 1), SPLIT_PART(tbl.col123, '.', 3) FROM table AS tbl""",
            write={
                "databricks": """select STRTOK('a_b_c'), STRTOK(tbl.col123, '.', 3) FROM table tbl;""",
            },
        )
        # # Test case to validate the static String and delimiter
        self.validate_all_transpiled(
            """SELECT SPLIT_PART('user@example.com', '@.', 2), SPLIT_PART(col123, '.', 1) FROM table AS tbl""",
            write={
                "databricks": """select STRTOK('user@example.com', '@.', 2),
                SPLIT_PART(col123, '.', 1) FROM table tbl;""",
            },
        )

    def test_tochar(self):
        # Test case to validate TO_CHAR conversion
        self.validate_all_transpiled(
            """SELECT TO_CHAR(column1, '">"$99.0"<"') AS D2_1, TO_CHAR(column1, '">"B9,999.0"<"') AS D4_1 FROM table""",
            write={
                "databricks": """select to_char(column1, '">"$99.0"<"') as D2_1,
                to_char(column1, '">"B9,999.0"<"') as D4_1 FROM table;""",
            },
        )

    def test_tovarchar(self):
        # Test case to validate TO_VARCHAR conversion
        self.validate_all_transpiled(
            """SELECT TO_CHAR(-12454.8, '99,999.9S'), '>' || TO_CHAR(col1, '00000.00') || '<' FROM dummy""",
            write={
                "databricks": """select to_varchar(-12454.8, '99,999.9S'),
                '>' || to_char(col1, '00000.00') || '<' FROM dummy;""",
            },
        )

    def test_timestampadd(self):
        # Test case to validate `TIMESTAMPADD` (alias to `DATEADD`) table column conversion
        self.validate_all_transpiled(
            """SELECT DATEADD(hour, -1, bp.ts) AND DATEADD(day, 2, bp.ts) FROM base_prep AS bp""",
            write={
                "databricks": """SELECT timestampadd('hour', -1, bp.ts) AND timestampadd('day', 2, bp.ts)
                FROM base_prep AS bp;""",
            },
        )
        # Test case to validate `DATEADD` `DATE` conversion quoted unit 'day'
        self.validate_all_transpiled(
            """SELECT DATEADD(day, 3, CAST('2020-02-03' AS DATE))""",
            write={
                "databricks": """select dateadd('day', 3, '2020-02-03'::date);""",
            },
        )
        # Test case to validate `TIMESTAMPADD` conversion
        self.validate_all_transpiled(
            """SELECT DATEADD(year, -3, '2023-02-03')""",
            write={
                "databricks": """select timestampadd(year, -3, '2023-02-03');""",
            },
        )
        # Test case to validate `TIMESTAMPADD` `TIMESTAMP` conversion
        self.validate_all_transpiled(
            """SELECT DATEADD(year, -3, CAST('2023-02-03 01:02' AS TIMESTAMP))""",
            write={
                "databricks": """select timestampadd(year, -3, '2023-02-03 01:02'::timestamp);""",
            },
        )
        # Test case to validate `TIMEADD` `TIMESTAMP` conversion
        self.validate_all_transpiled(
            """SELECT DATEADD(year, -3, CAST('2023-02-03 01:02' AS TIMESTAMP))""",
            write={
                "databricks": """select timeadd(year, -3, '2023-02-03 01:02'::timestamp);""",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `timestampadd` conversion of column:
            # unit, value, expr args are mandatory: `timestampadd(unit, value, expr)`
            self.validate_all_transpiled(
                "SELECT DATEADD(col1) AS timestampadd_col1 FROM tabl",
                write={
                    "databricks": "SELECT timestampadd(col1) AS timestampadd_col1 FROM tabl;",
                },
            )

    def test_timestampdiff(self):
        # Test case to validate TIMESTAMPDIFF (alias to DATEDIFF) timestamp conversion
        self.validate_all_transpiled(
            """SELECT DATEDIFF(month, CAST('2021-01-01' AS TIMESTAMP), CAST('2021-02-28' AS TIMESTAMP))""",
            write={
                "databricks": """select timestampDIFF(month, '2021-01-01'::timestamp, '2021-02-28'::timestamp);""",
            },
        )
        # Test case to validate `TIMESTAMPDIFF` conversion (quoted Unit 'month')
        self.validate_all_transpiled(
            """SELECT DATEDIFF(month, CAST('2021-01-01' AS TIMESTAMP), CAST('2021-02-28' AS TIMESTAMP))""",
            write={
                "databricks": """select timestampDIFF('month', '2021-01-01'::timestamp, '2021-02-28'::timestamp);""",
            },
        )
        # Test case to validate `DATEDIFF` `TIMESTAMP` conversion
        self.validate_all_transpiled(
            """SELECT DATEDIFF(day, CAST('2020-02-03' AS TIMESTAMP), CAST('2023-10-26' AS TIMESTAMP))""",
            write={
                "databricks": """select datediff('day', '2020-02-03'::timestamp, '2023-10-26'::timestamp);""",
            },
        )

    def test_try_to_number(self):
        # Test case to validate `TRY_TO_DECIMAL` parsing with format
        self.validate_all_transpiled(
            """SELECT CAST(TRY_TO_NUMBER('$345', '$999.00') AS DECIMAL(38, 0)) AS col1""",
            write={
                "databricks": """SELECT TRY_TO_DECIMAL('$345', '$999.00') AS col1""",
            },
        )
        # Test case to validate `TRY_TO_NUMERIC` parsing with format
        self.validate_all_transpiled(
            """SELECT CAST(TRY_TO_NUMBER('$345', '$999.99') AS DECIMAL(38, 0)) AS num""",
            write={
                "databricks": """SELECT TRY_TO_NUMERIC('$345', '$999.99') AS num""",
            },
        )
        # Test case to validate `TRY_TO_NUMBER` parsing with format
        self.validate_all_transpiled(
            """SELECT CAST(TRY_TO_NUMBER('$345', '$999.99') AS DECIMAL(38, 0)) AS num""",
            write={
                "databricks": """SELECT TRY_TO_NUMBER('$345', '$999.99') AS num""",
            },
        )
        # Test case to validate `TRY_TO_DECIMAL`, `TRY_TO_NUMERIC` parsing with format from table columns
        self.validate_all_transpiled(
            """SELECT CAST(TRY_TO_NUMBER(col1, '$999.099') AS DECIMAL(38, 0)),
            CAST(TRY_TO_NUMBER(tbl.col2, '$999,099.99') AS DECIMAL(38, 0)) FROM dummy AS tbl""",
            write={
                "databricks": """SELECT TRY_TO_DECIMAL(col1, '$999.099'),
                TRY_TO_NUMERIC(tbl.col2, '$999,099.99') FROM dummy tbl""",
            },
        )
        # Test case to validate `TRY_TO_NUMERIC` parsing with format, precision and scale from static string
        self.validate_all_transpiled(
            """SELECT CAST(TRY_TO_NUMBER('$345', '$999.99') AS DECIMAL(5, 2)) AS num_with_scale""",
            write={
                "databricks": """SELECT TRY_TO_NUMERIC('$345', '$999.99', 5, 2) AS num_with_scale""",
            },
        )
        # Test case to validate `TRY_TO_DECIMAL` parsing with format, precision and scale from static string
        self.validate_all_transpiled(
            """SELECT CAST(TRY_TO_NUMBER('$755', '$999.00') AS DECIMAL(15, 5)) AS num_with_scale""",
            write={
                "databricks": """SELECT TRY_TO_DECIMAL('$755', '$999.00', 15, 5) AS num_with_scale""",
            },
        )
        # Test case to validate `TRY_TO_NUMERIC`, `TRY_TO_NUMBER` parsing with format,
        # precision and scale from table columns
        self.validate_all_transpiled(
            """SELECT CAST(TRY_TO_NUMBER(sm.col1, '$999.00') AS DECIMAL(15, 5)) AS col1,
            CAST(TRY_TO_NUMBER(sm.col2, '$99.00') AS DECIMAL(15, 5)) AS col2 FROM sales_reports AS sm""",
            write={
                "databricks": """SELECT TRY_TO_NUMERIC(sm.col1, '$999.00', 15, 5) AS col1,
                TRY_TO_NUMBER(sm.col2, '$99.00', 15, 5) AS col2 FROM sales_reports sm""",
            },
        )

    def test_monthname(self):
        # Test case to validate `monthname` parsing of timestamp column
        self.validate_all_transpiled(
            """SELECT DATE_FORMAT(TO_TIMESTAMP('2015-04-03 10:00:00', 'yyyy-MM-dd HH:mm:ss'), 'MMM') AS MONTH""",
            write={
                "databricks": """SELECT MONTHNAME(TO_TIMESTAMP('2015-04-03 10:00:00')) AS MONTH;""",
            },
        )
        # Test case to validate `monthname` parsing of date column
        self.validate_all_transpiled(
            """SELECT DATE_FORMAT(TO_DATE('2015-05-01'), 'MMM') AS MONTH""",
            write={
                "databricks": """SELECT MONTHNAME(TO_DATE('2015-05-01')) AS MONTH;""",
            },
        )
        # Test case to validate `monthname` parsing of date column
        self.validate_all_transpiled(
            """SELECT DATE_FORMAT(TO_DATE('2020-01-01'), 'MMM') AS MONTH""",
            write={
                "databricks": """SELECT MONTH_NAME(TO_DATE('2020-01-01')) AS MONTH;""",
            },
        )
        # Test case to validate `monthname` parsing of string column with hours and minutes
        self.validate_all_transpiled(
            """SELECT DATE_FORMAT('2015-04-03 10:00', 'MMM') AS MONTH""",
            write={
                "databricks": """SELECT MONTHNAME('2015-04-03 10:00') AS MONTH;""",
            },
        )
        # Test case to validate `monthname` parsing of table column
        self.validate_all_transpiled(
            """SELECT d, DATE_FORMAT(d, 'MMM') FROM dates""",
            write={
                "databricks": """SELECT d, MONTHNAME(d) FROM dates;""",
            },
        )
        # Test case to validate `monthname` parsing of string column
        self.validate_all_transpiled(
            """SELECT DATE_FORMAT('2015-03-04', 'MMM') AS MON""",
            write={
                "databricks": """SELECT MONTHNAME('2015-03-04') AS MON;""",
            },
        )

        with self.assertRaises(ParseError):
            self.validate_all_transpiled(
                """SELECT DATE_FORMAT('2015-04-03 10:00', 'MMM') AS MONTH""",
                write={
                    "databricks": """SELECT DAYNAME('2015-04-03 10:00', 'MMM') AS MONTH;""",
                },
            )

        # Test case to validate `date_format` parsing of string column with custom format
        self.validate_all_transpiled(
            """SELECT DATE_FORMAT('2015.03.04', 'yyyy.dd.MM') AS MON""",
            write={
                "databricks": """SELECT DATE_FORMAT('2015.03.04', 'yyyy.dd.MM') AS MON;""",
            },
        )

    def test_zeroifnull(self):
        # Test case to validate `zeroifnull` conversion
        self.validate_all_transpiled(
            """SELECT IF(col1 IS NULL, 0, col1) AS pcol1 FROM tabl""",
            write={
                "databricks": """SELECT zeroifnull(col1) AS pcol1 FROM tabl;""",
            },
        )

    def test_nullifzero(self):
        # Test case to validate `nullifzero` conversion
        self.validate_all_transpiled(
            """SELECT t.n, IF(t.n = 0, NULL, t.n) AS pcol1 FROM tbl AS t""",
            write={
                "databricks": """SELECT t.n, nullifzero(t.n) AS pcol1 FROM tbl t;""",
            },
        )

    def test_square(self):
        self.validate_all_transpiled(
            "SELECT POWER(1, 2)",
            write={
                "databricks": "select square(1);",
            },
        )

        self.validate_all_transpiled(
            "SELECT POWER(-2, 2)",
            write={
                "databricks": "select square(-2);",
            },
        )

        self.validate_all_transpiled(
            "SELECT POWER(3.15, 2)",
            write={
                "databricks": "select SQUARE(3.15);",
            },
        )

        self.validate_all_transpiled(
            "SELECT POWER(NULL, 2)",
            write={
                "databricks": "select SQUARE(null);",
            },
        )

    def test_to_boolean(self):
        self.validate_all_transpiled(
            """SELECT
    CASE
       WHEN col1 IS NULL THEN NULL
       WHEN TYPEOF(col1) = 'boolean' THEN BOOLEAN(col1)
       WHEN TYPEOF(col1) = 'string' THEN
           CASE
               WHEN LOWER(col1) IN ('true', 't', 'yes', 'y', 'on', '1') THEN TRUE
               WHEN LOWER(col1) IN ('false', 'f', 'no', 'n', 'off', '0') THEN FALSE
               ELSE RAISE_ERROR('Boolean value of x is not recognized by TO_BOOLEAN')
               END
       WHEN ISNOTNULL(TRY_CAST(col1 AS DOUBLE)) THEN
           CASE
               WHEN ISNAN(CAST(col1 AS DOUBLE)) OR CAST(col1 AS DOUBLE) = DOUBLE('infinity') THEN
                    RAISE_ERROR('Invalid parameter type for TO_BOOLEAN')
               ELSE CAST(col1 AS DOUBLE) != 0.0
               END
       ELSE RAISE_ERROR('Invalid parameter type for TO_BOOLEAN')
       END""",
            write={
                "databricks": "select TO_BOOLEAN(col1);",
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

    def test_array_cat(self):
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

    def test_array_to_string(self):
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

    def test_split_part(self):
        self.validate_all_transpiled(
            "SELECT SPLIT_PART(col1, ',', 1)",
            write={
                "databricks": "SELECT SPLIT_PART(col1, ',', 0)",
            },
        )
        self.validate_all_transpiled(
            "SELECT SPLIT_PART(NULL, ',', 1)",
            write={
                "databricks": "SELECT SPLIT_PART(NULL, ',', 0)",
            },
        )
        self.validate_all_transpiled(
            "SELECT SPLIT_PART(col1, ',', 5)",
            write={
                "databricks": "SELECT SPLIT_PART(col1, ',', 5)",
            },
        )
        self.validate_all_transpiled(
            "SELECT SPLIT_PART('lit_string', ',', 1)",
            write={
                "databricks": "SELECT SPLIT_PART('lit_string', ',', 1)",
            },
        )
        self.validate_all_transpiled(
            "SELECT SPLIT_PART('lit_string', '', 1)",
            write={
                "databricks": "SELECT SPLIT_PART('lit_string', '', 1)",
            },
        )
        self.validate_all_transpiled(
            "SELECT SPLIT_PART(col1, 'delim', IF(LENGTH('abc') = 0, 1, LENGTH('abc')))",
            write={
                "databricks": "SELECT SPLIT_PART(col1, 'delim', len('abc'))",
            },
        )

        with self.assertRaises(ParseError):
            self.validate_all_transpiled(
                "SELECT SPLIT_PART('lit_string', ',', 5)",
                write={
                    "databricks": "SELECT SPLIT_PART('lit_string', ',')",
                },
            )

        with self.assertRaises(ParseError):
            # Test case to validate `split_part` conversion of column: ParseError
            # 3 arguments are needed: split_part(str, delim, partNum)
            self.validate_all_transpiled(
                "SELECT SPLIT_PART(col1) AS split_part_col1 FROM tabl",
                write={
                    "databricks": "SELECT split_part(col1) AS split_part_col1 FROM tabl;",
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
            "ALTER TABLE tab1 ADD COLUMN c2 DECIMAL(38, 0)",
            write={
                "databricks": "ALTER TABLE tab1 ADD COLUMN c2 NUMBER",
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

    def test_parse_json_extract_path_text(self):
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

        with self.assertRaises(ParseError):
            self.validate_all_transpiled(
                "SELECT GET_JSON_OBJECT('{}', CONCAT('$.', path_col)) FROM demo1",
                write={
                    "databricks": "SELECT JSON_EXTRACT_PATH_TEXT('{}') FROM demo1;",
                },
            )

    def test_uuid_string(self):
        self.validate_all_transpiled(
            "SELECT UUID()",
            write={
                "databricks": "SELECT UUID_STRING()",
            },
        )

        self.validate_all_transpiled(
            "SELECT UUID('fe971b24-9572-4005-b22f-351e9c09274d', 'foo')",
            write={
                "databricks": "SELECT UUID_STRING('fe971b24-9572-4005-b22f-351e9c09274d','foo')",
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

    def test_object_construct(self):
        self.validate_all_transpiled(
            "SELECT STRUCT(1 AS a, 'BBBB' AS b, NULL AS c)",
            write={
                "databricks": "SELECT OBJECT_CONSTRUCT('a',1,'b','BBBB', 'c',null);",
            },
        )
        self.validate_all_transpiled(
            "SELECT STRUCT(*) AS oc FROM demo_table_1",
            write={
                "databricks": "SELECT OBJECT_CONSTRUCT(*) AS oc FROM demo_table_1 ;",
            },
        )
        self.validate_all_transpiled(
            "SELECT STRUCT(*) FROM VALUES (1, 'x'), (2, 'y')",
            write={
                "databricks": "SELECT OBJECT_CONSTRUCT(*) FROM VALUES(1,'x'), (2,'y');",
            },
        )
        self.validate_all_transpiled(
            "SELECT STRUCT(FROM_JSON('NULL', {NULL_SCHEMA}) AS Key_One, "
            "NULL AS Key_Two, 'null' AS Key_Three) AS obj",
            write={
                "databricks": "SELECT OBJECT_CONSTRUCT('Key_One', PARSE_JSON('NULL'), 'Key_Two', "
                "NULL, 'Key_Three', 'null') as obj;",
            },
        )

    def test_object_keys(self):
        self.validate_all_transpiled(
            "SELECT JSON_OBJECT_KEYS(object1), JSON_OBJECT_KEYS(variant1) FROM objects_1 ORDER BY id NULLS LAST",
            write={
                "databricks": """
                                SELECT OBJECT_KEYS(object1), OBJECT_KEYS(variant1)
                                FROM objects_1
                                ORDER BY id;
                              """,
            },
        )
        self.validate_all_transpiled(
            "SELECT JSON_OBJECT_KEYS(FROM_JSON(column1, {COLUMN1_SCHEMA})) AS keys FROM table ORDER BY 1 NULLS LAST",
            write={
                "databricks": """
                                SELECT OBJECT_KEYS (
                                       PARSE_JSON (
                                           column1
                                           )
                                       ) AS keys
                                FROM table
                                ORDER BY 1;
                              """,
            },
        )

    def test_sum(self):
        # Test case to validate `sum` conversion of column
        self.validate_all_transpiled(
            "SELECT SUM(col1) AS sum_col1 FROM tabl",
            write={
                "databricks": "SELECT sum(col1) AS sum_col1 FROM tabl;",
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

    def test_nvl(self):
        # Test case to validate `nvl` conversion of column
        self.validate_all_transpiled(
            "SELECT COALESCE(col1, col2) AS nvl_col FROM tabl",
            write={
                "databricks": "SELECT nvl(col1, col2) AS nvl_col FROM tabl;",
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

    def test_nullif(self):
        # Test case to validate `nullif` conversion of column
        self.validate_all_transpiled(
            "SELECT NULLIF(col1, col2) AS nullif_col1 FROM tabl",
            write={
                "databricks": "SELECT nullif(col1, col2) AS nullif_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `nullif` conversion of column:
            # two columns / expressions are needed: nullif(expr1, expr2)
            self.validate_all_transpiled(
                "SELECT NULLIF(col1) AS nullif_col1 FROM tabl",
                write={
                    "databricks": "SELECT nullif(col1) AS nullif_col1 FROM tabl;",
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

    # [TODO]
    # Snowflake also takes an optional rounding mode argument.
    # Need to handle in transpiler using round and bround function based on the mode.
    def test_round(self):
        # Test case to validate `round` conversion of column
        self.validate_all_transpiled(
            "SELECT ROUND(col1) AS round_col1 FROM tabl",
            write={
                "databricks": "SELECT round(col1) AS round_col1 FROM tabl;",
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

    def test_row_number(self):
        # Test case to validate `row_number` conversion of column
        self.validate_all_transpiled(
            "SELECT symbol, exchange, shares, ROW_NUMBER() OVER (PARTITION BY exchange) AS row_number FROM trades",
            write={
                "databricks": "SELECT symbol, exchange, shares, ROW_NUMBER() OVER (PARTITION BY exchange) AS "
                "row_number FROM trades;",
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

    def test_upper(self):
        # Test case to validate `upper` conversion of column
        self.validate_all_transpiled(
            "SELECT UPPER(col1) AS upper_col1 FROM tabl",
            write={
                "databricks": "SELECT upper(col1) AS upper_col1 FROM tabl;",
            },
        )

    def test_trim(self):
        # Test case to validate `trim` conversion of column
        # [TODO]
        # Both Databricks and Snowflake can take an optional set of characters to be trimmed as parameter.
        # Need to handle that case.
        self.validate_all_transpiled(
            "SELECT TRIM(col1) AS trim_col1 FROM tabl",
            write={
                "databricks": "SELECT trim(col1) AS trim_col1 FROM tabl;",
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

    def test_join(self):
        # Test case to validate `any_value` conversion of column
        self.validate_all_transpiled(
            "SELECT t1.c1, t2.c2 FROM t1 JOIN t2 USING (c3)",
            write={
                "databricks": "SELECT t1.c1, t2.c2 FROM t1 JOIN t2 USING (c3)",
            },
        )

        self.validate_all_transpiled(
            "SELECT * FROM table1, table2 WHERE table1.column_name = table2.column_name",
            write={
                "databricks": "SELECT * FROM table1, table2 WHERE table1.column_name = table2.column_name",
            },
        )

    def test_try_cast(self):
        # Test case to validate `try_cast` conversion of static string
        self.validate_all_transpiled(
            "SELECT TRY_CAST('10' AS DECIMAL(38, 0))",
            write={
                "databricks": "SELECT try_cast('10' AS INT);",
            },
        )
        # Test case to validate `try_cast` conversion of column
        self.validate_all_transpiled(
            "SELECT TRY_CAST(col1 AS DOUBLE) AS try_cast_col1 FROM tabl",
            write={
                "databricks": "SELECT try_cast(col1 AS FLOAT) AS try_cast_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `try_cast` conversion of column: ParseError
            # sourceExpr and targetType are mandatory: try_cast(sourceExpr AS targetType)
            self.validate_all_transpiled(
                "SELECT TRY_CAST(col1) AS try_cast_col1 FROM tabl",
                write={
                    "databricks": "SELECT try_cast(col1) AS try_cast_col1 FROM tabl;",
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

    def test_replace(self):
        # Test case to validate `replace` conversion of column
        self.validate_all_transpiled(
            "SELECT REPLACE('ABC_abc', 'abc', 'DEF')",
            write={
                "databricks": "SELECT replace('ABC_abc', 'abc', 'DEF');",
            },
        )

    # [TODO]
    # In Snowflake, this function is overloaded; it can also be used as a numeric function to round down numeric
    # expressions. Also, it can take data time parts which are not supported in Databricks TRUNC function.
    # It may be transpiled to DATE_TRUNK function in Databricks.
    def test_trunc(self):
        # Test case to validate `trunc` conversion of column
        self.validate_all_transpiled(
            "SELECT TRUNC(col1, 'YEAR') AS trunc_col1 FROM tabl",
            write={
                "databricks": "SELECT trunc(col1, 'YEAR') AS trunc_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `trunc` conversion error:
            # UNIT is a mandatory argument: `trunc(expr, unit)`
            self.validate_all_transpiled(
                "SELECT TRUNC(col1) AS trunc_col1 FROM tabl",
                write={
                    "databricks": "SELECT trunc(col1) AS trunc_col1 FROM tabl;",
                },
            )

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
    def test_regexp_replace(self):
        # Test case to validate `regexp_replace` conversion of column
        self.validate_all_transpiled(
            "SELECT REGEXP_REPLACE(col1, '(\\d+)', '***') AS regexp_replace_col1 FROM tabl",
            write={
                "databricks": "SELECT regexp_replace(col1, '(\\d+)', '***') AS regexp_replace_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `regexp_replace` conversion of column: ParseError
            # `str, regexp, rep` are mandatory. `position` is Optional
            # `regexp_replace(str, regexp, rep [, position] )`
            self.validate_all_transpiled(
                "SELECT REGEXP_REPLACE(col1) AS regexp_replace_col1 FROM tabl",
                write={
                    "databricks": "SELECT regexp_replace(col1) AS regexp_replace_col1 FROM tabl;",
                },
            )

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

    def test_sqrt(self):
        # Test case to validate `sqrt` conversion of column
        self.validate_all_transpiled(
            "SELECT SQRT(col1) AS sqrt_col1 FROM tabl",
            write={
                "databricks": "SELECT sqrt(col1) AS sqrt_col1 FROM tabl;",
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

    def test_percentile_disc(self):
        # Test case to validate `percentile_disc` conversion of column
        self.validate_all_transpiled(
            "SELECT PERCENTILE_DISC(col1) AS percentile_disc_col1 FROM tabl",
            write={
                "databricks": "SELECT percentile_disc(col1) AS percentile_disc_col1 FROM tabl;",
            },
        )

    # [TODO]
    # REGEXP_SUBSTR in Snowflake takes various parameters some of which are not supported in Databricks' REGEXP_EXTRACT
    # function. Need to handle this case.
    def test_regexp_substr(self):
        # Test case to validate `regexp_substr` conversion of column
        self.validate_all_transpiled(
            "SELECT REGEXP_EXTRACT(col1, '(E|e)rror') AS regexp_substr_col1 FROM tabl",
            write={
                "databricks": "SELECT regexp_substr(col1, '(E|e)rror') AS regexp_substr_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `regexp_substr` conversion of column: ParseError
            # str, regexp args are mandatory: `regexp_substr( str, regexp )`
            self.validate_all_transpiled(
                "SELECT REGEXP_SUBSTR(col1) AS regexp_substr_col1 FROM tabl",
                write={
                    "databricks": "SELECT regexp_substr(col1) AS regexp_substr_col1 FROM tabl;",
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

    def test_rank(self):
        # Test case to validate `rank` conversion of column
        self.validate_all_transpiled(
            "SELECT RANK(col1) AS rank_col1 FROM tabl",
            write={
                "databricks": "SELECT rank(col1) AS rank_col1 FROM tabl;",
            },
        )

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

    # [TODO]
    # The syntax POSITION( <expr1> IN <expr2> ) is not supported in locate. The transpiler converts position to locate.
    # There is a native position function in Databricks. We can use that. Needs to be handled.
    def test_position(self):
        # Test case to validate `position` conversion of column `position(substr, str [, pos] )`
        self.validate_all_transpiled(
            "SELECT LOCATE('exc', col1) AS position_col1 FROM tabl",
            write={
                "databricks": "SELECT position('exc', col1) AS position_col1 FROM tabl;",
            },
        )
        # # Test case to validate `position` conversion of column `position(subtr IN str)`
        # self.validate_all_transpiled(
        #     "SELECT LOCATE('exc' IN col1) AS position_col1 FROM tabl",
        #     write={
        #         "databricks": "SELECT position('exc' IN col1) AS position_col1 FROM tabl;",
        #     },
        # )
        with self.assertRaises(ParseError):
            # Test case to validate `position` conversion of column: ParseError
            # substr, str are mandatory, pos is Optional: `position(substr, str [, pos] )` or  `position(subtr IN str)`
            self.validate_all_transpiled(
                "SELECT POSITION(col1) AS position_col1 FROM tabl",
                write={
                    "databricks": "SELECT position(col1) AS position_col1 FROM tabl;",
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

    def test_right(self):
        # Test case to validate `right` conversion of column
        self.validate_all_transpiled(
            "SELECT RIGHT(col1, 5) AS right_col1 FROM tabl",
            write={
                "databricks": "SELECT right(col1, 5) AS right_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `right` conversion of column: ParseError
            # str, len both are needed: `right(str, len)`
            self.validate_all_transpiled(
                "SELECT RIGHT(col1) AS left_col1 FROM tabl",
                write={
                    "databricks": "SELECT right(col1) AS left_col1 FROM tabl;",
                },
            )

    def test_mode(self):
        # Test case to validate `mode` conversion of column
        self.validate_all_transpiled(
            "SELECT MODE(col1) AS mode_col1 FROM tabl",
            write={
                "databricks": "SELECT mode(col1) AS mode_col1 FROM tabl;",
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

    def test_rpad(self):
        # Test case to validate `rpad` conversion of column
        self.validate_all_transpiled(
            "SELECT RPAD('hi', 5, 'ab')",
            write={
                "databricks": "SELECT rpad('hi', 5, 'ab');",
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

    def test_ntile(self):
        # Test case to validate `ntile` conversion of column
        self.validate_all_transpiled(
            "SELECT NTILE(col1) AS ntile_col1 FROM tabl",
            write={
                "databricks": "SELECT ntile(col1) AS ntile_col1 FROM tabl;",
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

    def test_to_timestamp(self):
        # Test case to validate `to_timestamp` conversion of column
        self.validate_all_transpiled(
            "SELECT CAST(col1 AS TIMESTAMP) AS to_timestamp_col1 FROM tabl",
            write={
                "databricks": "SELECT to_timestamp(col1) AS to_timestamp_col1 FROM tabl;",
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

    def test_percentile_cont(self):
        # Test case to validate `percentile_cont` conversion of column
        self.validate_all_transpiled(
            "SELECT PERCENTILE_CONT(col1) AS percentile_cont_col1 FROM tabl",
            write={
                "databricks": "SELECT percentile_cont(col1) AS percentile_cont_col1 FROM tabl;",
            },
        )

    def test_percent_rank(self):
        # Test case to validate `percent_rank` conversion of column
        self.validate_all_transpiled(
            "SELECT PERCENT_RANK() AS percent_rank_col1 FROM tabl",
            write={
                "databricks": "SELECT percent_rank() AS percent_rank_col1 FROM tabl;",
            },
        )

    def test_stddev(self):
        # Test case to validate `stddev` conversion of column
        self.validate_all_transpiled(
            "SELECT STDDEV(col1) AS stddev_col1 FROM tabl",
            write={
                "databricks": "SELECT stddev(col1) AS stddev_col1 FROM tabl;",
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

    def test_mod(self):
        # Test case to validate `mod` conversion of column
        self.validate_all_transpiled(
            "SELECT MOD(col1) AS mod_col1 FROM tabl",
            write={
                "databricks": "SELECT mod(col1) AS mod_col1 FROM tabl;",
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

    def test_radians(self):
        # Test case to validate `radians` conversion of column
        self.validate_all_transpiled(
            "SELECT RADIANS(col1) AS radians_col1 FROM tabl",
            write={
                "databricks": "SELECT radians(col1) AS radians_col1 FROM tabl;",
            },
        )

    # [TODO]
    # Both Databricks and Snowflake can take an optional set of characters to be trimmed as parameter.
    # Need to handle that case.
    def test_rtrim(self):
        # Test case to validate `rtrim` conversion of column
        self.validate_all_transpiled(
            "SELECT RTRIM(col1) AS rtrim_col1 FROM tabl",
            write={
                "databricks": "SELECT rtrim(col1) AS rtrim_col1 FROM tabl;",
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

    def test_startswith(self):
        # Test case to validate `startswith` conversion of column
        self.validate_all_transpiled(
            "SELECT STARTSWITH(col1, 'Spark') AS startswith_col1 FROM tabl",
            write={
                "databricks": "SELECT startswith(col1, 'Spark') AS startswith_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `startswith` conversion of column: ParseError
            # expr, startExpr both args are mandatory: `startswith(expr, startExpr)`
            self.validate_all_transpiled(
                "SELECT STARTSWITH(col1) AS startswith_col1 FROM tabl",
                write={
                    "databricks": "SELECT startswith(col1) AS startswith_col1 FROM tabl;",
                },
            )

    # [TODO]
    # The regex format may differ between Snowflake and Databricks. Needs manual intervention.
    # Also Snowflake may take optional regex parameters.
    # We may put a warning message so that users can validate manually.
    def test_regexp_like(self):
        # Test case to validate `regexp_like` conversion of column
        self.validate_all_transpiled(
            "SELECT col1 RLIKE '\\Users.*' AS regexp_like_col1 FROM tabl",
            write={
                "databricks": "SELECT regexp_like(col1, '\\Users.*') AS regexp_like_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `regexp_like` conversion of column
            # str, regex args are mandatory: `regexp_like( str, regex )`
            self.validate_all_transpiled(
                "SELECT REGEXP_LIKE(col1) AS regexp_like_col1 FROM tabl",
                write={
                    "databricks": "SELECT regexp_like(col1) AS regexp_like_col1 FROM tabl;",
                },
            )

    # [TODO]
    # Behavior of PARSE_URL is different in Snowflake and Databricks.
    # Need to handle it accordingly.
    def test_parse_url(self):
        # Test case to validate `parse_url` conversion of column
        self.validate_all_transpiled(
            "SELECT PARSE_URL(col1) AS parse_url_col1 FROM tabl",
            write={
                "databricks": "SELECT parse_url(col1) AS parse_url_col1 FROM tabl;",
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

    def test_reverse(self):
        # Test case to validate `reverse` conversion of column
        self.validate_all_transpiled(
            "SELECT REVERSE(col1) AS reverse_col1 FROM tabl",
            write={
                "databricks": "SELECT reverse(col1) AS reverse_col1 FROM tabl;",
            },
        )

    def test_ln(self):
        # Test case to validate `ln` conversion of column
        self.validate_all_transpiled(
            "SELECT LN(col1) AS ln_col1 FROM tabl",
            write={
                "databricks": "SELECT ln(col1) AS ln_col1 FROM tabl;",
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

    def test_random(self):
        # Test case to validate `random` conversion of column
        self.validate_all_transpiled(
            "SELECT RANDOM(), RANDOM(col1) FROM tabl",
            write={
                "databricks": "SELECT random(), random(col1) FROM tabl;",
            },
        )

    def test_sign(self):
        # Test case to validate `sign` conversion of column
        self.validate_all_transpiled(
            "SELECT SIGN(col1) AS sign_col1 FROM tabl",
            write={
                "databricks": "SELECT sign(col1) AS sign_col1 FROM tabl;",
            },
        )

    def test_sin(self):
        # Test case to validate `sin` conversion of column
        self.validate_all_transpiled(
            "SELECT SIN(col1) AS sin_col1 FROM tabl",
            write={
                "databricks": "SELECT sin(col1) AS sin_col1 FROM tabl;",
            },
        )

    def test_to_json(self):
        # Test case to validate `to_json` conversion of column
        self.validate_all_transpiled(
            "SELECT TO_JSON(col1) AS to_json_col1 FROM tabl",
            write={
                "databricks": "SELECT to_json(col1) AS to_json_col1 FROM tabl;",
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

    def test_stddev_pop(self):
        # Test case to validate `stddev_pop` conversion of column
        self.validate_all_transpiled(
            "SELECT STDDEV_POP(col1) AS stddev_pop_col1 FROM tabl",
            write={
                "databricks": "SELECT stddev_pop(col1) AS stddev_pop_col1 FROM tabl;",
            },
        )

    # [TODO]
    # Snowflake version takes optional parameters.
    # Show warning message if applicable.
    def test_regexp_count(self):
        # Test case to validate `regexp_count` conversion of column
        self.validate_all_transpiled(
            "SELECT REGEXP_COUNT(col1) AS regexp_count_col1 FROM tabl",
            write={
                "databricks": "SELECT regexp_count(col1) AS regexp_count_col1 FROM tabl;",
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

    # [TODO]
    # Snowflake version takes optional arguments.
    # Need to handle with a warning message if those arguments are passed.
    def test_regexp_instr(self):
        # Test case to validate `regexp_instr` conversion of column
        self.validate_all_transpiled(
            "SELECT REGEXP_INSTR(col1) AS regexp_instr_col1 FROM tabl",
            write={
                "databricks": "SELECT regexp_instr(col1) AS regexp_instr_col1 FROM tabl;",
            },
        )

    def test_repeat(self):
        # Test case to validate `repeat` conversion of column
        self.validate_all_transpiled(
            "SELECT REPEAT(col1, 5) AS repeat_col1 FROM tabl",
            write={
                "databricks": "SELECT repeat(col1, 5) AS repeat_col1 FROM tabl;",
            },
        )

        with self.assertRaises(ParseError):
            # Test case to validate `repeat` conversion of column: ParseError
            # expr, n times both are needed:  `repeat(expr, n)`
            self.validate_all_transpiled(
                "SELECT REPEAT(col1) AS repeat_col1 FROM tabl",
                write={
                    "databricks": "SELECT repeat(col1) AS repeat_col1 FROM tabl;",
                },
            )

    def test_nvl2(self):
        # Test case to validate `nvl2` conversion of static expressions
        self.validate_all_transpiled(
            "SELECT NVL2(NULL, 2, 1)",
            write={
                "databricks": "SELECT nvl2(NULL, 2, 1);",
            },
        )
        # Test case to validate `nvl2` conversion of column
        self.validate_all_transpiled(
            "SELECT NVL2(cond, col1, col2) AS nvl2_col1 FROM tabl",
            write={
                "databricks": "SELECT nvl2(cond, col1, col2) AS nvl2_col1 FROM tabl;",
            },
        )
        with self.assertRaises(ParseError):
            # Test case to validate `nvl2` conversion of column: ParseError
            # 3 arguments are needed: `nvl2(expr1, expr2, expr3)`
            self.validate_all_transpiled(
                "SELECT NVL2(col1) AS nvl2_col1 FROM tabl",
                write={
                    "databricks": "SELECT nvl2(col1) AS nvl2_col1 FROM tabl;",
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

    def test_pi(self):
        # Test case to validate `pi` conversion of column
        self.validate_all_transpiled(
            "SELECT PI() AS pi_col1 FROM tabl",
            write={
                "databricks": "SELECT PI() AS pi_col1 FROM tabl;",
            },
        )

    def test_stddev_samp(self):
        # Test case to validate `stddev_samp` conversion of column
        self.validate_all_transpiled(
            "SELECT STDDEV_SAMP(col1) AS stddev_samp_col1 FROM tabl",
            write={
                "databricks": "SELECT stddev_samp(col1) AS stddev_samp_col1 FROM tabl;",
            },
        )

    def test_tan(self):
        # Test case to validate `tan` conversion of column
        self.validate_all_transpiled(
            "SELECT TAN(col1) AS tan_col1 FROM tabl",
            write={
                "databricks": "SELECT tan(col1) AS tan_col1 FROM tabl;",
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

    def test_next_day(self):
        # Test case to validate `next_day` conversion of column
        self.validate_all_transpiled(
            "SELECT NEXT_DAY('2015-01-14', 'TU') AS next_day_col1 FROM tabl",
            write={
                "databricks": "SELECT next_day('2015-01-14', 'TU') AS next_day_col1 FROM tabl;",
            },
        )

    def test_regr_intercept(self):
        # Test case to validate `regr_intercept` conversion of column
        self.validate_all_transpiled(
            "SELECT REGR_INTERCEPT(v, v2) AS regr_intercept_col1 FROM tabl",
            write={
                "databricks": "SELECT regr_intercept(v, v2) AS regr_intercept_col1 FROM tabl;",
            },
        )

    def test_regr_r2(self):
        # Test case to validate `regr_r2` conversion of column
        self.validate_all_transpiled(
            "SELECT REGR_R2(v, v2) AS regr_r2_col1 FROM tabl",
            write={
                "databricks": "SELECT regr_r2(v, v2) AS regr_r2_col1 FROM tabl;",
            },
        )

    def test_regr_slope(self):
        # Test case to validate `regr_slope` conversion of column
        self.validate_all_transpiled(
            "SELECT REGR_SLOPE(v, v2) AS regr_slope_col1 FROM tabl",
            write={
                "databricks": "SELECT regr_slope(v, v2) AS regr_slope_col1 FROM tabl;",
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

    def test_translate(self):
        # Test case to validate `translate` conversion of column
        self.validate_all_transpiled(
            "SELECT TRANSLATE('AaBbCc', 'abc', '123') AS translate_col1 FROM tabl",
            write={
                "databricks": "SELECT translate('AaBbCc', 'abc', '123') AS translate_col1 FROM tabl;",
            },
        )

    def test_typeof(self):
        # Test case to validate `typeof` conversion of column
        self.validate_all_transpiled(
            "SELECT TYPEOF(col1) AS typeof_col1 FROM tabl",
            write={
                "databricks": "SELECT typeof(col1) AS typeof_col1 FROM tabl;",
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

    # [TODO]
    # Snowflake supports FROM { FIRST | LAST }
    # Need to handle this if FROM LAST is used in the query
    def test_nth_value(self):
        # Test case to validate `nth_value` conversion of column
        self.validate_all_transpiled(
            "SELECT NTH_VALUE(col1) AS nth_value_col1 FROM tabl",
            write={
                "databricks": "SELECT nth_value(col1) AS nth_value_col1 FROM tabl;",
            },
        )

    def test_parse_json(self):
        # Test case to validate `parse_json` conversion of column
        self.validate_all_transpiled(
            "SELECT tt.id, FROM_JSON(tt.details, {TT.DETAILS_SCHEMA}) FROM prod.public.table AS tt",
            write={
                "databricks": "SELECT tt.id, PARSE_JSON(tt.details) FROM prod.public.table tt;",
            },
        )
        # Test case to validate `parse_json` conversion of column
        self.validate_all_transpiled(
            "SELECT col1, FROM_JSON(col2, {COL2_SCHEMA}) FROM tabl",
            write={
                "databricks": "SELECT col1, TRY_PARSE_JSON(col2) FROM tabl;",
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

        with self.assertRaises(ParseError):
            self.validate_all_transpiled(
                """SELECT DATE_FORMAT('2015-04-03 10:00', 'E') AS MONTH""",
                write={
                    "databricks": """SELECT DAYNAME('2015-04-03 10:00', 'EEE') AS MONTH;""",
                },
            )

    def test_to_number(self):
        # Test case to validate `TO_DECIMAL` parsing with format
        self.validate_all_transpiled(
            """SELECT CAST(TO_NUMBER('$345', '$999.00') AS DECIMAL(38, 0)) AS col1""",
            write={
                "databricks": """SELECT TO_DECIMAL('$345', '$999.00') AS col1""",
            },
        )
        # Test case to validate `TO_NUMERIC` parsing with format
        self.validate_all_transpiled(
            """SELECT CAST(TO_NUMBER('$345', '$999.99') AS DECIMAL(38, 0)) AS num""",
            write={
                "databricks": """SELECT TO_NUMERIC('$345', '$999.99') AS num""",
            },
        )
        # Test case to validate `TO_NUMBER` parsing with format
        self.validate_all_transpiled(
            """SELECT CAST(TO_NUMBER('$345', '$999.99') AS DECIMAL(38, 0)) AS num""",
            write={
                "databricks": """SELECT TO_NUMBER('$345', '$999.99') AS num""",
            },
        )
        # Test case to validate `TO_DECIMAL`, `TO_NUMERIC` parsing with format from table columns
        self.validate_all_transpiled(
            """SELECT CAST(TO_NUMBER(col1, '$999.099') AS DECIMAL(38, 0)),
            CAST(TO_NUMBER(tbl.col2, '$999,099.99') AS DECIMAL(38, 0)) FROM dummy AS tbl""",
            write={
                "databricks": """SELECT TO_DECIMAL(col1, '$999.099'),
                TO_NUMERIC(tbl.col2, '$999,099.99') FROM dummy tbl""",
            },
        )
        # Test case to validate `TO_NUMERIC` parsing with format, precision and scale from static string
        self.validate_all_transpiled(
            """SELECT CAST(TO_NUMBER('$345', '$999.99') AS DECIMAL(5, 2)) AS num_with_scale""",
            write={
                "databricks": """SELECT TO_NUMERIC('$345', '$999.99', 5, 2) AS num_with_scale""",
            },
        )
        # Test case to validate `TO_DECIMAL` parsing with format, precision and scale from static string
        self.validate_all_transpiled(
            """SELECT CAST(TO_NUMBER('$755', '$999.00') AS DECIMAL(15, 5)) AS num_with_scale""",
            write={
                "databricks": """SELECT TO_DECIMAL('$755', '$999.00', 15, 5) AS num_with_scale""",
            },
        )
        # Test case to validate `TO_NUMERIC`, `TO_NUMBER` parsing with format, precision and scale from table columns
        self.validate_all_transpiled(
            """SELECT CAST(TO_NUMBER(sm.col1, '$999.00') AS DECIMAL(15, 5)) AS col1,
            CAST(TO_NUMBER(sm.col2, '$99.00') AS DECIMAL(15, 5)) AS col2 FROM sales_reports AS sm""",
            write={
                "databricks": """SELECT TO_NUMERIC(sm.col1, '$999.00', 15, 5) AS col1,
                TO_NUMBER(sm.col2, '$99.00', 15, 5) AS col2 FROM sales_reports sm""",
            },
        )

        with self.assertRaises(UnsupportedError):
            # Test case to validate `TO_DECIMAL` parsing without format
            self.validate_all_transpiled(
                """SELECT CAST(TO_NUMBER('$345', '$999.00') AS DECIMAL(38, 0)) AS col1""",
                write={
                    "databricks": """SELECT TO_DECIMAL('$345') AS col1""",
                },
            )

        with self.assertRaises(ParseError):
            self.validate_all_transpiled(
                """SELECT CAST(TO_NUMBER('$345', '$999.99') AS DECIMAL(5, 2)) AS num_with_scale""",
                write={
                    "databricks": """SELECT TO_NUMERIC('$345', '$999.99', 5, 2, 1) AS num_with_scale""",
                },
            )

    def test_to_time(self):
        # Test case to validate `TRY_TO_DATE` parsing with default format
        self.validate_all_transpiled(
            """SELECT TO_TIMESTAMP('2018-05-15', 'yyyy-MM-d')""",
            write={
                "databricks": """SELECT TO_TIME('2018-05-15', 'yyyy-MM-dd')""",
            },
        )
        # Test case to validate `TRY_TO_DATE` parsing with default format
        self.validate_all_transpiled(
            """SELECT TO_TIMESTAMP('2018-05-15 00:01:02', 'yyyy-MM-dd HH:mm:ss')""",
            write={
                "databricks": """SELECT TO_TIME('2018-05-15 00:01:02')""",
            },
        )

    def test_timestamp_from_parts(self):
        self.validate_all_transpiled(
            """SELECT MAKE_TIMESTAMP(1992, 6, 1, 12, 35, 12)""",
            write={
                "databricks": """select timestamp_from_parts(1992, 6, 1, 12, 35, 12);""",
            },
        )
        self.validate_all_transpiled(
            """SELECT MAKE_TIMESTAMP(2023, 10, 3, 14, 10, 45), MAKE_TIMESTAMP(2020, 4, 4, 4, 5, 6)""",
            write={
                "databricks": """select TIMESTAMP_FROM_PARTS(2023, 10, 3, 14, 10, 45),
                timestamp_from_parts(2020, 4, 4, 4, 5, 6);""",
            },
        )

    def test_to_variant(self):
        self.validate_all_transpiled(
            """SELECT TO_JSON(col1) AS json_col1 FROM dummy""",
            write={
                "databricks": """SELECT to_variant(col1) AS json_col1 FROM dummy;""",
            },
        )

    def test_to_array(self):
        self.validate_all_transpiled(
            """SELECT IF(col1 IS NULL, NULL, ARRAY(col1)) AS ary_col""",
            write={
                "databricks": """SELECT to_array(col1) AS ary_col;""",
            },
        )

    def test_to_rlike(self):
        self.validate_all_transpiled(
            r"""SELECT '800-456-7891' RLIKE '[2-9]\d{2}-\d{3}-\d{4}' AS matches_phone_number""",
            write={
                "databricks": """SELECT RLIKE('800-456-7891','[2-9]\\d{2}-\\d{3}-\\d{4}') AS matches_phone_number;;""",
            },
        )

    def test_try_to_boolean(self):
        self.validate_all_transpiled(
            """SELECT
    CASE
       WHEN 1 IS NULL THEN NULL
       WHEN TYPEOF(1) = 'boolean' THEN BOOLEAN(1)
       WHEN TYPEOF(1) = 'string' THEN
           CASE
               WHEN LOWER(1) IN ('true', 't', 'yes', 'y', 'on', '1') THEN TRUE
               WHEN LOWER(1) IN ('false', 'f', 'no', 'n', 'off', '0') THEN FALSE
               ELSE RAISE_ERROR('Boolean value of x is not recognized by TO_BOOLEAN')
               END
       WHEN ISNOTNULL(TRY_CAST(1 AS DOUBLE)) THEN
           CASE
               WHEN ISNAN(CAST(1 AS DOUBLE)) OR CAST(1 AS DOUBLE) = DOUBLE('infinity') THEN
                    RAISE_ERROR('Invalid parameter type for TO_BOOLEAN')
               ELSE CAST(1 AS DOUBLE) != 0.0
               END
       ELSE NULL
       END""",
            write={
                "databricks": "select TRY_TO_BOOLEAN(1);",
            },
        )

    def test_sysdate(self):
        self.validate_all_transpiled(
            "SELECT CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()",
            write={
                "databricks": """SELECT SYSDATE(), CURRENT_TIMESTAMP();""",
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

    def test_array_construct_compact(self):
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

    def test_to_double(self):
        self.validate_all_transpiled(
            "SELECT DOUBLE('HELLO')",
            write={
                "databricks": "SELECT TO_DOUBLE('HELLO')",
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

    def test_to_object(self):
        self.validate_all_transpiled(
            "SELECT TO_JSON(k) FROM tabl",
            write={
                "databricks": "SELECT to_object(k) FROM tabl",
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

    def test_create_ddl(self):
        self.validate_all_transpiled(
            """
                create table employee (employee_id decimal(38, 0),
                    first_name string not null,
                    last_name string not null,
                    birth_date date,
                    hire_date date,
                    salary decimal(10, 2),
                    department_id decimal(38, 0))
            """,
            write={
                "databricks": """
                    CREATE TABLE employee (employee_id INT,
                        first_name VARCHAR(50) NOT NULL,
                        last_name VARCHAR(50) NOT NULL,
                        birth_date DATE,
                        hire_date DATE,
                        salary DECIMAL(10, 2),
                        department_id INT)
                """,
            },
        )
