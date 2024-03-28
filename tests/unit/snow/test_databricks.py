"""
Test Cases to validate target Databricks dialect
"""

# pylint: disable=too-many-lines
import pytest
from sqlglot import ParseError, UnsupportedError


def test_struct(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate JSON to STRUCT conversion
    validate_source_transpile(
        databricks_sql="""SELECT STRUCT(1 AS a, 2 AS b), ARRAY(STRUCT(11 AS C, 22 AS d), 3)""",
        source={
            "snowflake": """SELECT {'a': 1, 'b': 2}, [{'c': 11, 'd': 22}, 3];""",
        },
    )


def test_lateral_struct(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        databricks_sql="""SELECT p.value.id AS `ID` FROM persons_struct AS p""",
        source={
            "snowflake": """SELECT p.value:id as "ID" FROM persons_struct p;""",
        },
    )
    validate_source_transpile(
        databricks_sql="""SELECT f.name AS `Contact`,
                      f.first,
                      CAST(p.value.id AS DOUBLE) AS `id_parsed`,
                      p.c.value.first,
                      p.value
               FROM persons_struct AS p\n LATERAL VIEW EXPLODE($p.$c.contact) AS f""",
        source={
            "snowflake": """SELECT f.value:name AS "Contact",
                                        f.value:first,
                                        p.value:id::FLOAT AS "id_parsed",
                                        p.c:value:first,
                                        p.value
                                 FROM persons_struct p, lateral flatten(input => ${p}.${c}, path => 'contact') f;""",
        },
    )
    validate_source_transpile(
        databricks_sql="""SELECT
                      CAST(d.value.display_position AS DECIMAL(38, 0)) AS item_card_impression_display_position,
                      CAST(i.impression_attributes AS STRING) AS item_card_impression_impression_attributes,
                      CAST(CURRENT_TIMESTAMP() AS TIMESTAMP) AS dwh_created_date_time_utc,
                      CAST(i.propensity AS DOUBLE) AS propensity, candidates
               FROM dwh.vw_replacement_customer AS d\n LATERAL VIEW OUTER EXPLODE(d.item_card_impressions) AS i
               WHERE event_date_pt = '{start_date}' AND event_name IN ('store.replacements_view')""",
        source={
            "snowflake": """SELECT d.value:display_position::NUMBER as item_card_impression_display_position,
                                   i.value:impression_attributes::VARCHAR as item_card_impression_impression_attributes,
                                   cast(current_timestamp() as timestamp_ntz(9)) as dwh_created_date_time_utc,
                                   i.value:propensity::FLOAT as propensity,
                                   candidates
                                 FROM dwh.vw_replacement_customer  d,
                                 LATERAL FLATTEN (INPUT => d.item_card_impressions, OUTER => TRUE) i
                                 WHERE event_date_pt = '{start_date}' and event_name in ('store.replacements_view')""",
        },
    )
    validate_source_transpile(
        databricks_sql="""SELECT tt.id AS tax_transaction_id,
                      CAST(tt.response_body.isMpfState AS BOOLEAN) AS is_mpf_state,
                      REGEXP_REPLACE(tt.request_body.deliveryLocation.city, '""', '') AS delivery_city,
                      REGEXP_REPLACE(tt.request_body.store.storeAddress.zipCode, '""', '') AS store_zipcode
               FROM tax_table AS tt""",
        source={
            "snowflake": """SELECT
                                   tt.id AS tax_transaction_id,
                                   cast(tt.response_body:"isMpfState" AS BOOLEAN) AS is_mpf_state,
                                   REGEXP_REPLACE(tt.request_body:"deliveryLocation":"city", '""', '') AS delivery_city,
                                   REGEXP_REPLACE(tt.request_body:"store":"storeAddress":"zipCode", '""', '') AS
                                   store_zipcode
                                   FROM tax_table  tt
                              """,
        },
    )
    validate_source_transpile(
        databricks_sql="""SELECT varchar1, CAST(float1 AS STRING), CAST(variant1.`Loan Number` AS STRING) FROM tmp""",
        source={
            "snowflake": """ select varchar1,
                                        float1::varchar,
                                        variant1:"Loan Number"::varchar from tmp;
                              """,
        },
    )
    validate_source_transpile(
        databricks_sql="""SELECT ARRAY_EXCEPT(ARRAY(STRUCT(1 AS a, 2 AS b), 1), ARRAY(STRUCT(1 AS a, 2 AS b), 3))""",
        source={
            "snowflake": """SELECT ARRAY_EXCEPT([{'a': 1, 'b': 2}, 1], [{'a': 1, 'b': 2}, 3]);""",
        },
    )
    validate_source_transpile(
        databricks_sql="""SELECT v, v.food, TO_JSON(v) FROM jdemo1""",
        source={
            "snowflake": """SELECT v, v:food, TO_JSON(v) FROM jdemo1;""",
        },
    )
    validate_source_transpile(
        databricks_sql="""SELECT STRIP_NULL_VALUE(src.c) FROM mytable""",
        source={
            "snowflake": """SELECT STRIP_NULL_VALUE(src:c) FROM mytable;""",
        },
    )
    validate_source_transpile(
        databricks_sql="""SELECT CAST(los.objectDomain AS STRING) AS object_type,
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
        source={
            "snowflake": """select
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
    validate_source_transpile(
        databricks_sql="""SELECT tt.id, FROM_JSON(tt.details, {TT.DETAILS_SCHEMA}) FROM prod.public.table AS tt 
        LATERAL VIEW EXPLODE(FROM_JSON(FROM_JSON(tt.resp, {TT.RESP_SCHEMA}).items, {JSON_COLUMN_SCHEMA})) AS lit
        LATERAL VIEW EXPLODE(FROM_JSON(lit.value.details, {JSON_COLUMN_SCHEMA})) AS ltd""",
        source={
            "snowflake": """
                SELECT
                tt.id
                , PARSE_JSON(tt.details)
                FROM prod.public.table tt
                ,  LATERAL FLATTEN (input=> PARSE_JSON(PARSE_JSON(tt.resp):items)) AS lit
                ,  LATERAL FLATTEN (input=> parse_json(lit.value:"details")) AS ltd;""",
        },
    )

    validate_source_transpile(
        "SELECT level_1_key.level_2_key['1'] FROM demo1",
        source={
            "snowflake": "SELECT level_1_key:level_2_key:'1' FROM demo1;",
        },
    )


def test_datediff(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate SF supported 'yrs' Date and Time Parts conversion
    validate_source_transpile(
        "SELECT DATEDIFF(year, CAST('2021-02-28 12:00:00' AS TIMESTAMP), CAST('2021-03-28 12:00:00' AS TIMESTAMP))",
        source={
            "snowflake": "SELECT datediff(yrs, TIMESTAMP'2021-02-28 12:00:00', TIMESTAMP'2021-03-28 12:00:00');",
        },
    )
    # Test case to validate SF supported 'years' Date and Time Parts conversion
    validate_source_transpile(
        "SELECT DATEDIFF(year, CAST('2021-02-28 12:00:00' AS TIMESTAMP), CAST('2021-03-28 12:00:00' AS TIMESTAMP))",
        source={
            "snowflake": "SELECT datediff(years, TIMESTAMP'2021-02-28 12:00:00', TIMESTAMP'2021-03-28 12:00:00');",
        },
    )
    # Test case to validate SF supported 'mm' Date and Time Parts conversion
    validate_source_transpile(
        "SELECT DATEDIFF(month, CAST('2021-02-28' AS DATE), CAST('2021-03-28' AS DATE))",
        source={
            "snowflake": "SELECT datediff(mm, DATE'2021-02-28', DATE'2021-03-28');",
        },
    )
    # Test case to validate SF supported 'mons' Date and Time Parts conversion
    validate_source_transpile(
        "SELECT DATEDIFF(month, CAST('2021-02-28' AS DATE), CAST('2021-03-28' AS DATE))",
        source={
            "snowflake": "SELECT datediff(mons, DATE'2021-02-28', DATE'2021-03-28');",
        },
    )
    # Test case to validate SF supported 'days' Date and Time Parts conversion
    validate_source_transpile(
        "SELECT DATEDIFF(day, 'start', 'end')",
        source={
            "snowflake": "SELECT datediff('days', 'start', 'end');",
        },
    )
    # Test case to validate SF supported 'dayofmonth' Date and Time Parts conversion
    validate_source_transpile(
        "SELECT DATEDIFF(day, 'start', 'end')",
        source={
            "snowflake": "SELECT datediff(dayofmonth, 'start', 'end');",
        },
    )
    # Test case to validate SF supported 'wk' Date and Time Parts conversion
    validate_source_transpile(
        "SELECT DATEDIFF(week, 'start', 'end')",
        source={
            "snowflake": "SELECT datediff(wk, 'start', 'end');",
        },
    )
    # Test case to validate SF supported 'woy' Date and Time Parts conversion
    validate_source_transpile(
        "SELECT DATEDIFF(week, 'start', 'end')",
        source={
            "snowflake": "SELECT datediff('woy', 'start', 'end');",
        },
    )
    # Test case to validate SF supported 'qtrs' Date and Time Parts conversion
    validate_source_transpile(
        "SELECT DATEDIFF(quarter, 'start', 'end')",
        source={
            "snowflake": "SELECT datediff('qtrs', 'start', 'end');",
        },
    )
    # Test case to validate SF supported 'quarters' Date and Time Parts conversion
    validate_source_transpile(
        "SELECT DATEDIFF(quarter, 'start', 'end')",
        source={
            "snowflake": "SELECT datediff(quarters, 'start', 'end');",
        },
    )
    validate_source_transpile(
        "SELECT DATEDIFF(day, 'end', 'start')",
        source={"snowflake": "SELECT DATEDIFF('start', 'end')"},
    )


def test_strtok_to_array(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate the static String and default delimiter
    validate_source_transpile(
        """SELECT SPLIT('my text is divided','[ ]')""",
        source={
            "snowflake": """select STRTOK_TO_ARRAY('my text is divided');""",
        },
    )
    # Test case to validate the conversion of static String and table column with delimiter
    validate_source_transpile(
        """SELECT SPLIT('v_p_n','[_]'), SPLIT(col123,'[.]') FROM table AS tbl""",
        source={
            "snowflake": """select STRTOK_TO_ARRAY('v_p_n', "_"), STRTOK_TO_ARRAY(col123, ".") FROM table tbl;""",
        },
    )
    # Test case to validate the static String and delimiter
    validate_source_transpile(
        """SELECT SPLIT('a@b.c','[.@]')""",
        source={
            "snowflake": """select STRTOK_TO_ARRAY('a@b.c', ".@");""",
        },
    )


def test_date_from_parts(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        """SELECT MAKE_DATE(1992, 6, 1)""",
        source={
            "snowflake": """select date_from_parts(1992, 6, 1);""",
        },
    )
    validate_source_transpile(
        """SELECT MAKE_DATE(2023, 10, 3), MAKE_DATE(2020, 4, 4)""",
        source={
            "snowflake": """select date_from_parts(2023, 10, 3), date_from_parts(2020, 4, 4);""",
        },
    )
    validate_source_transpile(
        """SELECT MAKE_DATE(2023, 10, 3), MAKE_DATE(2020, 4, 4)""",
        source={
            "snowflake": """select datefromparts(2023, 10, 3), datefromparts(2020, 4, 4);""",
        },
    )


def test_convert_timezone(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `convert_timezone` parsing with Src TZ, tgt TZ and String Timestamp
    validate_source_transpile(
        """SELECT CONVERT_TIMEZONE('America/Los_Angeles', 'America/New_York', '2019-01-01 14:00:00') AS conv""",
        source={
            "snowflake": """SELECT
                CONVERT_TIMEZONE('America/Los_Angeles', 'America/New_York', '2019-01-01 14:00:00'::timestamp_ntz)
                AS conv""",
        },
    )
    # Test case to validate `convert_timezone` parsing with tgt TZ and String Timestamp
    validate_source_transpile(
        """SELECT CONVERT_TIMEZONE('America/Los_Angeles', '2018-04-05 12:00:00 +02:00') AS conv""",
        source={
            "snowflake": """SELECT CONVERT_TIMEZONE('America/Los_Angeles', '2018-04-05 12:00:00 +02:00')
                AS conv""",
        },
    )
    # Test case to validate `convert_timezone` parsing with tgt TZ and Timestamp Column
    validate_source_transpile(
        """SELECT a.col1, CONVERT_TIMEZONE('IST', a.ts_col) AS conv_ts FROM dummy AS a""",
        source={
            "snowflake": """SELECT a.col1, CONVERT_TIMEZONE('IST', a.ts_col) AS conv_ts FROM dummy a""",
        },
    )
    # Test case to validate `convert_timezone` parsing with tgt TZ and Current Timestamp
    validate_source_transpile(
        """SELECT
        CURRENT_TIMESTAMP() AS now_in_la, CONVERT_TIMEZONE('America/New_York', CURRENT_TIMESTAMP()) AS now_in_nyc,
        CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP()) AS now_in_paris,
        CONVERT_TIMEZONE('Asia/Tokyo', CURRENT_TIMESTAMP()) AS now_in_tokyo""",
        source={
            "snowflake": """SELECT CURRENT_TIMESTAMP() AS now_in_la,
                CONVERT_TIMEZONE('America/New_York', CURRENT_TIMESTAMP()) AS now_in_nyc,
                CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP()) AS now_in_paris,
                CONVERT_TIMEZONE('Asia/Tokyo', CURRENT_TIMESTAMP()) AS now_in_tokyo;""",
        },
    )
    # Test case to validate `convert_timezone` parsing with src TZ, tgt TZ and String converted to Timestamp column
    validate_source_transpile(
        """SELECT CONVERT_TIMEZONE('Europe/Warsaw', 'UTC', '2019-01-01 00:00:00 +03:00')""",
        source={
            "snowflake": """SELECT
                CONVERT_TIMEZONE('Europe/Warsaw', 'UTC', '2019-01-01 00:00:00 +03:00'::timestamp_ntz);""",
        },
    )


def test_try_to_date(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `TRY_TO_DATE` parsing with default format
    validate_source_transpile(
        """SELECT DATE(TRY_TO_TIMESTAMP('2018-05-15', 'yyyy-MM-dd'))""",
        source={
            "snowflake": """SELECT TRY_TO_DATE('2018-05-15')""",
        },
    )
    # Test case to validate `TRY_TO_DATE` parsing with custom format
    validate_source_transpile(
        """SELECT DATE(TRY_TO_TIMESTAMP('2023-25-09', 'yyyy-dd-MM'))""",
        source={
            "snowflake": """SELECT TRY_TO_DATE('2023-25-09', 'yyyy-dd-MM')""",
        },
    )
    # Test case to validate `TRY_TO_DATE` String, column parsing with custom format
    validate_source_transpile(
        """SELECT DATE(TRY_TO_TIMESTAMP('2012.20.12', 'yyyy.dd.MM')),
        DATE(TRY_TO_TIMESTAMP(d.col1, 'yyyy-MM-dd')) FROM dummy AS d""",
        source={
            "snowflake": """SELECT TRY_TO_DATE('2012.20.12', 'yyyy.dd.MM'), TRY_TO_DATE(d.col1) FROM dummy d""",
        },
    )


def test_try_to_timestamp(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `TRY_TO_TIMESTAMP` parsing
    validate_source_transpile(
        """SELECT TRY_TO_TIMESTAMP('2016-12-31 00:12:00')""",
        source={
            "snowflake": """SELECT TRY_TO_TIMESTAMP('2016-12-31 00:12:00')""",
        },
    )
    # Test case to validate `TRY_TO_TIMESTAMP` String, column parsing with custom format
    validate_source_transpile(
        """SELECT TRY_TO_TIMESTAMP('2018-05-15', 'yyyy-MM-dd')""",
        source={
            "snowflake": """SELECT TRY_TO_TIMESTAMP('2018-05-15', 'yyyy-MM-dd')""",
        },
    )


def test_strtok(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate the static String, default delimiter (single space) and default partition number (1)
    validate_source_transpile(
        """SELECT SPLIT_PART('my text is divided', ' ', 1)""",
        source={
            "snowflake": """select STRTOK('my text is divided');""",
        },
    )
    # Test case to validate the static String, table column, delimiter and partition number
    validate_source_transpile(
        """SELECT SPLIT_PART('a_b_c', ' ', 1), SPLIT_PART(tbl.col123, '.', 3) FROM table AS tbl""",
        source={
            "snowflake": """select STRTOK('a_b_c'), STRTOK(tbl.col123, '.', 3) FROM table tbl;""",
        },
    )
    # # Test case to validate the static String and delimiter
    validate_source_transpile(
        """SELECT SPLIT_PART('user@example.com', '@.', 2), SPLIT_PART(col123, '.', 1) FROM table AS tbl""",
        source={
            "snowflake": """select STRTOK('user@example.com', '@.', 2),
                SPLIT_PART(col123, '.', 1) FROM table tbl;""",
        },
    )


def test_tochar(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate TO_CHAR conversion
    validate_source_transpile(
        """SELECT TO_CHAR(column1, '">"$99.0"<"') AS D2_1, TO_CHAR(column1, '">"B9,999.0"<"') AS D4_1 FROM table""",
        source={
            "snowflake": """select to_char(column1, '">"$99.0"<"') as D2_1,
                to_char(column1, '">"B9,999.0"<"') as D4_1 FROM table;""",
        },
    )


def test_tovarchar(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate TO_VARCHAR conversion
    validate_source_transpile(
        """SELECT TO_CHAR(-12454.8, '99,999.9S'), '>' || TO_CHAR(col1, '00000.00') || '<' FROM dummy""",
        source={
            "snowflake": """select to_varchar(-12454.8, '99,999.9S'),
                '>' || to_char(col1, '00000.00') || '<' FROM dummy;""",
        },
    )


def test_timestampadd(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `TIMESTAMPADD` (alias to `DATEADD`) table column conversion
    validate_source_transpile(
        """SELECT DATEADD(hour, -1, bp.ts) AND DATEADD(day, 2, bp.ts) FROM base_prep AS bp""",
        source={
            "snowflake": """SELECT timestampadd('hour', -1, bp.ts) AND timestampadd('day', 2, bp.ts)
                FROM base_prep AS bp;""",
        },
    )
    # Test case to validate `DATEADD` `DATE` conversion quoted unit 'day'
    validate_source_transpile(
        """SELECT DATEADD(day, 3, CAST('2020-02-03' AS DATE))""",
        source={
            "snowflake": """select dateadd('day', 3, '2020-02-03'::date);""",
        },
    )
    # Test case to validate `TIMESTAMPADD` conversion
    validate_source_transpile(
        """SELECT DATEADD(year, -3, '2023-02-03')""",
        source={
            "snowflake": """select timestampadd(year, -3, '2023-02-03');""",
        },
    )
    # Test case to validate `TIMESTAMPADD` `TIMESTAMP` conversion
    validate_source_transpile(
        """SELECT DATEADD(year, -3, CAST('2023-02-03 01:02' AS TIMESTAMP))""",
        source={
            "snowflake": """select timestampadd(year, -3, '2023-02-03 01:02'::timestamp);""",
        },
    )
    # Test case to validate `TIMEADD` `TIMESTAMP` conversion
    validate_source_transpile(
        """SELECT DATEADD(year, -3, CAST('2023-02-03 01:02' AS TIMESTAMP))""",
        source={
            "snowflake": """select timeadd(year, -3, '2023-02-03 01:02'::timestamp);""",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `timestampadd` conversion of column:
        # unit, value, expr args are mandatory: `timestampadd(unit, value, expr)`
        validate_source_transpile(
            "SELECT DATEADD(col1) AS timestampadd_col1 FROM tabl",
            source={
                "snowflake": "SELECT timestampadd(col1) AS timestampadd_col1 FROM tabl;",
            },
        )


def test_timestampdiff(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate TIMESTAMPDIFF (alias to DATEDIFF) timestamp conversion
    validate_source_transpile(
        """SELECT DATEDIFF(month, CAST('2021-01-01' AS TIMESTAMP), CAST('2021-02-28' AS TIMESTAMP))""",
        source={
            "snowflake": """select timestampDIFF(month, '2021-01-01'::timestamp, '2021-02-28'::timestamp);""",
        },
    )
    # Test case to validate `TIMESTAMPDIFF` conversion (quoted Unit 'month')
    validate_source_transpile(
        """SELECT DATEDIFF(month, CAST('2021-01-01' AS TIMESTAMP), CAST('2021-02-28' AS TIMESTAMP))""",
        source={
            "snowflake": """select timestampDIFF('month', '2021-01-01'::timestamp, '2021-02-28'::timestamp);""",
        },
    )
    # Test case to validate `DATEDIFF` `TIMESTAMP` conversion
    validate_source_transpile(
        """SELECT DATEDIFF(day, CAST('2020-02-03' AS TIMESTAMP), CAST('2023-10-26' AS TIMESTAMP))""",
        source={
            "snowflake": """select datediff('day', '2020-02-03'::timestamp, '2023-10-26'::timestamp);""",
        },
    )


def test_try_to_number(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `TRY_TO_DECIMAL` parsing with format
    validate_source_transpile(
        """SELECT CAST(TRY_TO_NUMBER('$345', '$999.00') AS DECIMAL(38, 0)) AS col1""",
        source={
            "snowflake": """SELECT TRY_TO_DECIMAL('$345', '$999.00') AS col1""",
        },
    )
    # Test case to validate `TRY_TO_NUMERIC` parsing with format
    validate_source_transpile(
        """SELECT CAST(TRY_TO_NUMBER('$345', '$999.99') AS DECIMAL(38, 0)) AS num""",
        source={
            "snowflake": """SELECT TRY_TO_NUMERIC('$345', '$999.99') AS num""",
        },
    )
    # Test case to validate `TRY_TO_NUMBER` parsing with format
    validate_source_transpile(
        """SELECT CAST(TRY_TO_NUMBER('$345', '$999.99') AS DECIMAL(38, 0)) AS num""",
        source={
            "snowflake": """SELECT TRY_TO_NUMBER('$345', '$999.99') AS num""",
        },
    )
    # Test case to validate `TRY_TO_DECIMAL`, `TRY_TO_NUMERIC` parsing with format from table columns
    validate_source_transpile(
        """SELECT CAST(TRY_TO_NUMBER(col1, '$999.099') AS DECIMAL(38, 0)),
        CAST(TRY_TO_NUMBER(tbl.col2, '$999,099.99') AS DECIMAL(38, 0)) FROM dummy AS tbl""",
        source={
            "snowflake": """SELECT TRY_TO_DECIMAL(col1, '$999.099'),
                TRY_TO_NUMERIC(tbl.col2, '$999,099.99') FROM dummy tbl""",
        },
    )
    # Test case to validate `TRY_TO_NUMERIC` parsing with format, precision and scale from static string
    validate_source_transpile(
        """SELECT CAST(TRY_TO_NUMBER('$345', '$999.99') AS DECIMAL(5, 2)) AS num_with_scale""",
        source={
            "snowflake": """SELECT TRY_TO_NUMERIC('$345', '$999.99', 5, 2) AS num_with_scale""",
        },
    )
    # Test case to validate `TRY_TO_DECIMAL` parsing with format, precision and scale from static string
    validate_source_transpile(
        """SELECT CAST(TRY_TO_NUMBER('$755', '$999.00') AS DECIMAL(15, 5)) AS num_with_scale""",
        source={
            "snowflake": """SELECT TRY_TO_DECIMAL('$755', '$999.00', 15, 5) AS num_with_scale""",
        },
    )
    # Test case to validate `TRY_TO_NUMERIC`, `TRY_TO_NUMBER` parsing with format,
    # precision and scale from table columns
    validate_source_transpile(
        """SELECT CAST(TRY_TO_NUMBER(sm.col1, '$999.00') AS DECIMAL(15, 5)) AS col1,
        CAST(TRY_TO_NUMBER(sm.col2, '$99.00') AS DECIMAL(15, 5)) AS col2 FROM sales_reports AS sm""",
        source={
            "snowflake": """SELECT TRY_TO_NUMERIC(sm.col1, '$999.00', 15, 5) AS col1,
                TRY_TO_NUMBER(sm.col2, '$99.00', 15, 5) AS col2 FROM sales_reports sm""",
        },
    )
    # Test case to validate `TRY_TO_DECIMAL` parsing without format
    validate_source_transpile(
        """SELECT CAST('$345' AS DECIMAL(38, 0)) AS str_col,
                  CAST(99.56854634 AS DECIMAL(38, 0)) AS num_col,
                  CAST(-4.35 AS DECIMAL(38, 0)) AS num_col1,
                  CAST(col1 AS DECIMAL(38, 0)) AS col1""",
        source={
            "snowflake": """SELECT TRY_TO_DECIMAL('$345') AS str_col,
                                   TRY_TO_DECIMAL(99.56854634) AS num_col,
                                   TRY_TO_DECIMAL(-4.35) AS num_col1,
                                   TRY_TO_DECIMAL(col1) AS col1""",
        },
    )


def test_monthname(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `monthname` parsing of timestamp column
    validate_source_transpile(
        """SELECT DATE_FORMAT(cast('2015-04-03 10:00:00' as timestamp), 'MMM') AS MONTH""",
        source={
            "snowflake": """SELECT MONTHNAME(TO_TIMESTAMP('2015-04-03 10:00:00')) AS MONTH;""",
        },
    )
    # Test case to validate `monthname` parsing of date column
    validate_source_transpile(
        """SELECT DATE_FORMAT(cast('2015-05-01' as date), 'MMM') AS MONTH""",
        source={
            "snowflake": """SELECT MONTHNAME(TO_DATE('2015-05-01')) AS MONTH;""",
        },
    )
    # Test case to validate `monthname` parsing of date column
    validate_source_transpile(
        """SELECT DATE_FORMAT(cast('2020-01-01' as date), 'MMM') AS MONTH""",
        source={
            "snowflake": """SELECT MONTH_NAME(TO_DATE('2020-01-01')) AS MONTH;""",
        },
    )
    # Test case to validate `monthname` parsing of string column with hours and minutes
    validate_source_transpile(
        """SELECT DATE_FORMAT('2015-04-03 10:00', 'MMM') AS MONTH""",
        source={
            "snowflake": """SELECT MONTHNAME('2015-04-03 10:00') AS MONTH;""",
        },
    )
    # Test case to validate `monthname` parsing of table column
    validate_source_transpile(
        """SELECT d, DATE_FORMAT(d, 'MMM') FROM dates""",
        source={
            "snowflake": """SELECT d, MONTHNAME(d) FROM dates;""",
        },
    )
    # Test case to validate `monthname` parsing of string column
    validate_source_transpile(
        """SELECT DATE_FORMAT('2015-03-04', 'MMM') AS MON""",
        source={
            "snowflake": """SELECT MONTHNAME('2015-03-04') AS MON;""",
        },
    )
    with pytest.raises(ParseError):
        # Snowflake expects only 1 argument for MonthName function
        validate_source_transpile(
            """SELECT DATE_FORMAT('2015-04-03 10:00', 'MMM') AS MONTH""",
            source={
                "snowflake": """SELECT MONTHNAME('2015-04-03 10:00', 'MMM') AS MONTH;""",
            },
        )

    with pytest.raises(ParseError):
        validate_source_transpile(
            """SELECT DATE_FORMAT('2015-04-03 10:00', 'MMM') AS MONTH""",
            source={
                "snowflake": """SELECT DAYNAME('2015-04-03 10:00', 'MMM') AS MONTH;""",
            },
        )

    # Test case to validate `date_format` parsing of string column with custom format
    validate_source_transpile(
        """SELECT DATE_FORMAT('2015.03.04', 'yyyy.dd.MM') AS MON""",
        source={
            "snowflake": """SELECT DATE_FORMAT('2015.03.04', 'yyyy.dd.MM') AS MON;""",
        },
    )


def test_zeroifnull(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `zeroifnull` conversion
    validate_source_transpile(
        """SELECT IF(col1 IS NULL, 0, col1) AS pcol1 FROM tabl""",
        source={
            "snowflake": """SELECT zeroifnull(col1) AS pcol1 FROM tabl;""",
        },
    )


def test_nullifzero(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `nullifzero` conversion
    validate_source_transpile(
        """SELECT t.n, IF(t.n = 0, NULL, t.n) AS pcol1 FROM tbl AS t""",
        source={
            "snowflake": """SELECT t.n, nullifzero(t.n) AS pcol1 FROM tbl t;""",
        },
    )


def test_square(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT POWER(1, 2)",
        source={
            "snowflake": "select square(1);",
        },
    )

    validate_source_transpile(
        "SELECT POWER(-2, 2)",
        source={
            "snowflake": "select square(-2);",
        },
    )

    validate_source_transpile(
        "SELECT POWER(3.15, 2)",
        source={
            "snowflake": "select SQUARE(3.15);",
        },
    )

    validate_source_transpile(
        "SELECT POWER(NULL, 2)",
        source={
            "snowflake": "select SQUARE(null);",
        },
    )


def test_to_boolean(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
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
        source={
            "snowflake": "select TO_BOOLEAN(col1);",
        },
    )


def test_charindex(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate CHARINDEX conversion
    validate_source_transpile(
        """SELECT CHARINDEX('an', 'banana', 3), CHARINDEX('ab', 'abababab'), n, h, CHARINDEX(n, h) FROM pos""",
        source={
            "snowflake": """select charindex('an', 'banana', 3),
                charindex('ab', 'abababab'), n, h, CHARINDEX(n, h) FROM pos;""",
        },
    )


def test_dateadd(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `DATEADD` `DATE` conversion quoted unit 'day'
    validate_source_transpile(
        """SELECT DATEADD(day, 3, CAST('2020-02-03' AS DATE))""",
        source={
            "snowflake": """select dateadd('day', 3, '2020-02-03'::date);""",
        },
    )


def test_is_integer(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        """SELECT
CASE
   WHEN col IS NULL THEN NULL
   WHEN col RLIKE '^-?[0-9]+$' AND TRY_CAST(col AS INT) IS NOT NULL THEN TRUE
   ELSE FALSE
   END""",
        source={
            "snowflake": "select IS_INTEGER(col);",
        },
    )


def test_arrayagg(dialect_context):
    validate_source_transpile, _ = dialect_context

    validate_source_transpile(
        """SELECT ARRAY_AGG(col1) FROM test_table""",
        source={
            "snowflake": """select array_agg(col1) FROM test_table;""",
        },
    )

    validate_source_transpile(
        """
            SELECT
              SORT_ARRAY(ARRAY_AGG(DISTINCT col2))
            FROM test_table
            WHERE
              col3 > 10000""",
        source={
            "snowflake": """
            SELECT ARRAY_AGG(DISTINCT col2) WITHIN GROUP (ORDER BY col2 ASC)
            FROM test_table
            WHERE col3 > 10000;""",
        },
    )

    validate_source_transpile(
        """
            SELECT
              SORT_ARRAY(ARRAY_AGG(col2))
            FROM test_table
            WHERE
              col3 > 10000""",
        source={
            "snowflake": """
            SELECT ARRAY_AGG(col2) WITHIN GROUP (ORDER BY col2 ASC)
            FROM test_table
            WHERE col3 > 10000;""",
        },
    )

    validate_source_transpile(
        """
            SELECT
              col2,
              TRANSFORM(ARRAY_SORT(ARRAY_AGG(NAMED_STRUCT('value', col4, 'sort_by', col3)),
                  (left, right) -> CASE
                                          WHEN left.sort_by < right.sort_by THEN 1
                                          WHEN left.sort_by > right.sort_by THEN -1
                                          ELSE 0
                                      END), s -> s.value)
            FROM test_table
            WHERE
              col3 > 450000
            GROUP BY
              col2
            ORDER BY
              col2 DESC NULLS FIRST""",
        source={
            "snowflake": """
              SELECT
                col2,
                ARRAYAGG(col4) WITHIN GROUP (ORDER BY col3 DESC)
              FROM test_table
              WHERE col3 > 450000
              GROUP BY col2
              ORDER BY col2 DESC;""",
        },
    )

    validate_source_transpile(
        """
            SELECT
              col2,
              TRANSFORM(ARRAY_SORT(ARRAY_AGG(NAMED_STRUCT('value', col4, 'sort_by', col3)),
                  (left, right) -> CASE
                                          WHEN left.sort_by < right.sort_by THEN -1
                                          WHEN left.sort_by > right.sort_by THEN 1
                                          ELSE 0
                                      END), s -> s.value)
            FROM test_table
            WHERE
              col3 > 450000
            GROUP BY
              col2
            ORDER BY
              col2 DESC NULLS FIRST""",
        source={
            "snowflake": """
              SELECT
                col2,
                ARRAYAGG(col4) WITHIN GROUP (ORDER BY col3)
              FROM test_table
              WHERE col3 > 450000
              GROUP BY col2
              ORDER BY col2 DESC;""",
        },
    )

    validate_source_transpile(
        """SELECT
              SORT_ARRAY(ARRAY_AGG(col2), FALSE)
            FROM test_table""",
        source={
            "snowflake": """SELECT ARRAY_AGG(col2) WITHIN GROUP (ORDER BY col2 DESC) FROM test_table;""",
        },
    )

    validate_source_transpile(
        """
        WITH cte AS (SELECT id, tag, SUM(tag.count) AS item_count FROM another_table) SELECT id,
        TRANSFORM(ARRAY_SORT(ARRAY_AGG(NAMED_STRUCT('value', tag, 'sort_by', item_count)), (left, right) -> CASE
                        WHEN left.sort_by < right.sort_by THEN 1
                        WHEN left.sort_by > right.sort_by THEN -1
                        ELSE 0
                    END), s -> s.value) AS agg_tags FROM cte GROUP BY 1
        """,
        source={
            "snowflake": """
            WITH cte AS (
              SELECT
                id,
                tag,
                SUM(tag:count) AS item_count
              FROM another_table
            )
            SELECT
            id
            , ARRAY_AGG(tag) WITHIN GROUP(ORDER BY item_count DESC) AS agg_tags
            FROM cte
            GROUP BY 1;
            """,
        },
    )

    with (pytest.raises(ParseError, match="both must refer to the same column"),):
        validate_source_transpile(
            """SELECT
                  SORT_ARRAY(ARRAY_AGG(DISTINCT col2), FALSE)
                FROM test_table""",
            source={
                "snowflake": """SELECT ARRAY_AGG(DISTINCT col2) WITHIN GROUP (ORDER BY col3 DESC) FROM test_table;""",
            },
        )


def test_array_cat(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `array_cat` conversion
    validate_source_transpile(
        """SELECT CONCAT(col1, col2) FROM tbl""",
        source={
            "snowflake": """select array_cat(col1, col2) FROM tbl;""",
        },
    )
    # Test case to validate `array_cat` conversion
    validate_source_transpile(
        """SELECT CONCAT(ARRAY(1, 3), ARRAY(2, 4))""",
        source={
            "snowflake": """select array_cat(array(1, 3), array(2, 4))""",
        },
    )


def test_array_to_string(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `ARRAY_TO_STRING` conversion
    validate_source_transpile(
        """SELECT ARRAY_JOIN(ary_column1, '') AS no_separation FROM tbl""",
        source={
            "snowflake": "SELECT ARRAY_TO_STRING(ary_column1, '') AS no_separation FROM tbl",
        },
    )


def test_listagg(dialect_context):
    validate_source_transpile, _ = dialect_context

    validate_source_transpile(
        """
        SELECT
          ARRAY_JOIN(ARRAY_AGG(col1), ' ')
        FROM test_table
        WHERE
          col2 > 10000
        """,
        source={
            "snowflake": "SELECT LISTAGG(col1, ' ') FROM test_table WHERE col2 > 10000;",
        },
    )

    validate_source_transpile(
        """
        SELECT
          ARRAY_JOIN(ARRAY_AGG(col1), '')
        FROM test_table
        """,
        source={
            "snowflake": "SELECT LISTAGG(col1) FROM test_table;",
        },
    )

    validate_source_transpile(
        """
        SELECT
          ARRAY_JOIN(ARRAY_AGG(DISTINCT col3), '|')
        FROM test_table
        WHERE
          col2 > 10000
        """,
        source={
            "snowflake": """SELECT LISTAGG(DISTINCT col3, '|')
            FROM test_table WHERE col2 > 10000;""",
        },
    )

    validate_source_transpile(
        """
        SELECT
          col3,
          ARRAY_JOIN(TRANSFORM(ARRAY_SORT(ARRAY_AGG(NAMED_STRUCT('value', col4, 'sort_by', col2)),
                (left, right) -> CASE
                                        WHEN left.sort_by < right.sort_by THEN 1
                                        WHEN left.sort_by > right.sort_by THEN -1
                                        ELSE 0
                                    END), s -> s.value), ', ')
        FROM test_table
        WHERE
          col2 > 10000
        GROUP BY
          col3
        """,
        source={
            "snowflake": """
            SELECT col3, listagg(col4, ', ') WITHIN GROUP (ORDER BY col2 DESC)
            FROM
            test_table
            WHERE col2 > 10000 GROUP BY col3;
            """,
        },
    )


def test_collate(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT ENDSWITH(COLLATE('ñn', 'sp'), COLLATE('n', 'sp'))",
        source={
            "snowflake": "SELECT ENDSWITH(COLLATE('ñn', 'sp'), COLLATE('n', 'sp'));",
        },
    )

    validate_source_transpile(
        "SELECT v, COLLATION(v), COLLATE(v, 'sp-upper'), COLLATION(COLLATE(v, 'sp-upper')) FROM collation1",
        source={
            "snowflake": "SELECT v, COLLATION(v), COLLATE(v, 'sp-upper'), COLLATION(COLLATE(v, 'sp-upper')) "
            "FROM collation1;",
        },
    )


def test_split_part(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT SPLIT_PART(col1, ',', 1)",
        source={
            "snowflake": "SELECT SPLIT_PART(col1, ',', 0)",
        },
    )
    validate_source_transpile(
        "SELECT SPLIT_PART(NULL, ',', 1)",
        source={
            "snowflake": "SELECT SPLIT_PART(NULL, ',', 0)",
        },
    )
    validate_source_transpile(
        "SELECT SPLIT_PART(col1, ',', 5)",
        source={
            "snowflake": "SELECT SPLIT_PART(col1, ',', 5)",
        },
    )
    validate_source_transpile(
        "SELECT SPLIT_PART('lit_string', ',', 1)",
        source={
            "snowflake": "SELECT SPLIT_PART('lit_string', ',', 1)",
        },
    )
    validate_source_transpile(
        "SELECT SPLIT_PART('lit_string', '', 1)",
        source={
            "snowflake": "SELECT SPLIT_PART('lit_string', '', 1)",
        },
    )
    validate_source_transpile(
        "SELECT SPLIT_PART(col1, 'delim', IF(LENGTH('abc') = 0, 1, LENGTH('abc')))",
        source={
            "snowflake": "SELECT SPLIT_PART(col1, 'delim', len('abc'))",
        },
    )

    with pytest.raises(ParseError):
        validate_source_transpile(
            "SELECT SPLIT_PART('lit_string', ',', 5)",
            source={
                "snowflake": "SELECT SPLIT_PART('lit_string', ',')",
            },
        )

    with pytest.raises(ParseError):
        # Test case to validate `split_part` conversion of column: ParseError
        # 3 arguments are needed: split_part(str, delim, partNum)
        validate_source_transpile(
            "SELECT SPLIT_PART(col1) AS split_part_col1 FROM tabl",
            source={
                "snowflake": "SELECT split_part(col1) AS split_part_col1 FROM tabl;",
            },
        )


def test_tablesample(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT * FROM (SELECT * FROM example_table) TABLESAMPLE (1 PERCENT) REPEATABLE (99)",
        source={
            "snowflake": "select * from (select * from example_table) sample (1) seed (99);",
        },
    )

    validate_source_transpile(
        "SELECT * FROM (SELECT * FROM example_table) TABLESAMPLE (1 PERCENT) REPEATABLE (99)",
        source={
            "snowflake": "select * from (select * from example_table) tablesample (1) seed (99);",
        },
    )

    validate_source_transpile(
        "SELECT * FROM (SELECT * FROM t1 JOIN t2 ON t1.a = t2.c) TABLESAMPLE (1 PERCENT)",
        source={
            "snowflake": """
    select *
       from (
             select *
                from t1 join t2
                   on t1.a = t2.c
            ) sample (1);
                """,
        },
    )


def test_skip_unsupported_operations(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "",
        source={
            "snowflake": "ALTER SESSION SET QUERY_TAG = 'tag1';",
        },
    )

    validate_source_transpile(
        "",
        source={
            "snowflake": "BEGIN;",
        },
    )

    validate_source_transpile(
        "",
        source={
            "snowflake": "ROLLBACK;",
        },
    )

    validate_source_transpile(
        "",
        source={
            "snowflake": "COMMIT;",
        },
    )

    validate_source_transpile(
        "",
        source={
            "snowflake": "CREATE STREAM mystream ON TABLE mytable;",
        },
    )

    validate_source_transpile(
        "",
        source={
            "snowflake": "ALTER STREAM mystream SET COMMENT = 'New comment for stream';",
        },
    )

    validate_source_transpile(
        "",
        source={
            "snowflake": "SHOW STREAMS LIKE 'line%' IN tpch.public;",
        },
    )

    validate_source_transpile(
        "ALTER TABLE tab1 ADD COLUMN c2 DECIMAL(38, 0)",
        source={
            "snowflake": "ALTER TABLE tab1 ADD COLUMN c2 NUMBER",
        },
    )

    validate_source_transpile(
        "",
        source={
            "snowflake": """
                CREATE TASK t1
                  SCHEDULE = '60 MINUTE'
                  TIMESTAMP_INPUT_FORMAT = 'YYYY-MM-DD HH24'
                  USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL'
                AS
                INSERT INTO mytable(ts) VALUES(CURRENT_TIMESTAMP);
                """,
        },
    )

    validate_source_transpile(
        "",
        source={
            "snowflake": "EXECUTE TASK mytask;",
        },
    )

    validate_source_transpile(
        "SELECT DISTINCT dst.CREATED_DATE, dst.task_id, CAST(dd.delivery_id AS STRING) AS delivery_id, "
        "dst.ISSUE_CATEGORY, dst.issue, dd.store_id FROM proddb.public.dimension_salesforce_tasks AS dst JOIN "
        "edw.finance.dimension_deliveries AS dd ON dd.delivery_id = dst.delivery_id /* this ensures delivery_id "
        "is associated */ WHERE dst.mto_flag = 1 AND dst.customer_type IN ('Consumer') AND dd.STORE_ID IN (SELECT "
        "store_id FROM foo.bar.cng_stores_stage) AND dd.is_test = FALSE AND dst.origin IN ('Chat') AND NOT "
        "dd_agent_id IS NULL AND dst.CREATED_DATE > CURRENT_DATE - 7 ORDER BY 1 DESC NULLS FIRST, 3 DESC NULLS "
        "FIRST",
        source={
            "snowflake": """
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


def test_div0null(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT IF(b = 0 OR b IS NULL, 0, a / b)",
        source={
            "snowflake": "SELECT DIV0NULL(a, b)",
        },
    )


def test_div0(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT IF(b = 0, 0, a / b)",
        source={
            "snowflake": "SELECT DIV0(a, b)",
        },
    )


def test_parse_json_extract_path_text(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT GET_JSON_OBJECT(json_data, '$.level_1_key.level_2_key[1]') FROM demo1",
        source={
            "snowflake": "SELECT JSON_EXTRACT_PATH_TEXT(json_data, 'level_1_key.level_2_key[1]') FROM demo1;",
        },
    )

    validate_source_transpile(
        "SELECT GET_JSON_OBJECT(json_data, CONCAT('$.', path_col)) FROM demo1",
        source={
            "snowflake": "SELECT JSON_EXTRACT_PATH_TEXT(json_data, path_col) FROM demo1;",
        },
    )

    validate_source_transpile(
        "SELECT GET_JSON_OBJECT('{}', CONCAT('$.', path_col)) FROM demo1",
        source={
            "snowflake": "SELECT JSON_EXTRACT_PATH_TEXT('{}', path_col) FROM demo1;",
        },
    )

    with pytest.raises(ParseError):
        validate_source_transpile(
            "SELECT GET_JSON_OBJECT('{}', CONCAT('$.', path_col)) FROM demo1",
            source={
                "snowflake": "SELECT JSON_EXTRACT_PATH_TEXT('{}') FROM demo1;",
            },
        )


def test_uuid_string(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT UUID()",
        source={
            "snowflake": "SELECT UUID_STRING()",
        },
    )

    validate_source_transpile(
        "SELECT UUID('fe971b24-9572-4005-b22f-351e9c09274d', 'foo')",
        source={
            "snowflake": "SELECT UUID_STRING('fe971b24-9572-4005-b22f-351e9c09274d','foo')",
        },
    )


def test_bitor_agg(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT BIT_OR(k) FROM bitwise_example",
        source={
            "snowflake": "select bitor_agg(k) from bitwise_example",
        },
    )

    validate_source_transpile(
        "SELECT s2, BIT_OR(k) FROM bitwise_example GROUP BY s2",
        source={
            "snowflake": "select s2, bitor_agg(k) from bitwise_example group by s2",
        },
    )


def test_object_construct(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT STRUCT(1 AS a, 'BBBB' AS b, NULL AS c)",
        source={
            "snowflake": "SELECT OBJECT_CONSTRUCT('a',1,'b','BBBB', 'c',null);",
        },
    )
    validate_source_transpile(
        "SELECT STRUCT(*) AS oc FROM demo_table_1",
        source={
            "snowflake": "SELECT OBJECT_CONSTRUCT(*) AS oc FROM demo_table_1 ;",
        },
    )
    validate_source_transpile(
        "SELECT STRUCT(*) FROM VALUES (1, 'x'), (2, 'y')",
        source={
            "snowflake": "SELECT OBJECT_CONSTRUCT(*) FROM VALUES(1,'x'), (2,'y');",
        },
    )
    validate_source_transpile(
        "SELECT STRUCT(FROM_JSON('NULL', {json_column_schema}) AS Key_One, NULL AS Key_Two, 'null' AS Key_Three) AS obj",
        source={
            "snowflake": "SELECT OBJECT_CONSTRUCT('Key_One', PARSE_JSON('NULL'), 'Key_Two', "
            "NULL, 'Key_Three', 'null') as obj;",
        },
    )


def test_object_keys(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT JSON_OBJECT_KEYS(object1), JSON_OBJECT_KEYS(variant1) FROM objects_1 ORDER BY id NULLS LAST",
        source={
            "snowflake": """
                                SELECT OBJECT_KEYS(object1), OBJECT_KEYS(variant1)
                                FROM objects_1
                                ORDER BY id;
                              """,
        },
    )
    validate_source_transpile(
        "SELECT JSON_OBJECT_KEYS(FROM_JSON(column1, {COLUMN1_SCHEMA})) AS keys FROM table ORDER BY 1 NULLS LAST",
        source={
            "snowflake": """
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


def test_sum(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `sum` conversion of column
    validate_source_transpile(
        "SELECT SUM(col1) AS sum_col1 FROM tabl",
        source={
            "snowflake": "SELECT sum(col1) AS sum_col1 FROM tabl;",
        },
    )


def test_coalesce(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `coalesce` conversion of column
    validate_source_transpile(
        "SELECT COALESCE(col1, col2) AS coalesce_col FROM tabl",
        source={
            "snowflake": "SELECT coalesce(col1, col2) AS coalesce_col FROM tabl;",
        },
    )


def test_nvl(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `nvl` conversion of column
    validate_source_transpile(
        "SELECT COALESCE(col1, col2) AS nvl_col FROM tabl",
        source={
            "snowflake": "SELECT nvl(col1, col2) AS nvl_col FROM tabl;",
        },
    )


def test_count(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `count` conversion of column
    validate_source_transpile(
        "SELECT COUNT(col1) AS count_col1 FROM tabl",
        source={
            "snowflake": "SELECT count(col1) AS count_col1 FROM tabl;",
        },
    )

    # [TODO]
    # Snowflake supports various date time parts
    # https://docs.snowflake.com/en/sql-reference/functions-date-time#label-supported-date-time-parts
    # Need to handle these in transpiler


def test_date_trunc(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `date_trunc` conversion of static string
    validate_source_transpile(
        "SELECT DATE_TRUNC('YEAR', '2015-03-05T09:32:05.359')",
        source={
            "snowflake": "SELECT date_trunc('YEAR', '2015-03-05T09:32:05.359');",
        },
    )
    # Test Date Trunc with TRY_TO_DATE patch 119
    validate_source_transpile(
        "DELETE FROM table1 WHERE cre_at >= DATE_TRUNC('MONTH', DATE(TRY_TO_TIMESTAMP('2022-01-15', 'yyyy-MM-dd')));",
        source={
            "snowflake": "DELETE FROM table1 WHERE cre_at >= DATE_TRUNC('month', TRY_TO_DATE('2022-01-15'));",
        },
    )

    validate_source_transpile(
        "SELECT DATE_TRUNC('MONTH', DATE(TRY_TO_TIMESTAMP(COLUMN1, 'yyyy-MM-dd'))) FROM table",
        source={
            "snowflake": "select DATE_TRUNC('month', TRY_TO_DATE(COLUMN1)) from table;",
        },
    )

    # Test case to validate `date_trunc` conversion of column
    validate_source_transpile(
        "SELECT DATE_TRUNC('MONTH', col1) AS date_trunc_col1 FROM tabl",
        source={
            "snowflake": "SELECT date_trunc('MM', col1) AS date_trunc_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `date_trunc` conversion error:
        # UNIT is a mandatory argument: `date_trunc(unit, expr)`
        validate_source_transpile(
            "SELECT DATE_TRUNC(col1) AS date_trunc_col1 FROM tabl",
            source={
                "snowflake": "SELECT date_trunc(col1) AS date_trunc_col1 FROM tabl;",
            },
        )


def test_nullif(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `nullif` conversion of column
    validate_source_transpile(
        "SELECT NULLIF(col1, col2) AS nullif_col1 FROM tabl",
        source={
            "snowflake": "SELECT nullif(col1, col2) AS nullif_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `nullif` conversion of column:
        # two columns / expressions are needed: nullif(expr1, expr2)
        validate_source_transpile(
            "SELECT NULLIF(col1) AS nullif_col1 FROM tabl",
            source={
                "snowflake": "SELECT nullif(col1) AS nullif_col1 FROM tabl;",
            },
        )


def test_iff(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `iff` conversion of column
    validate_source_transpile(
        "SELECT IF(cond, col1, col2) AS iff_col1 FROM tabl",
        source={
            "snowflake": "SELECT iff(cond, col1, col2) AS iff_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `iff` conversion of column:
        # three arguments are needed (iff(cond, expr1, expr2)
        validate_source_transpile(
            "SELECT IFF(col1) AS iff_col1 FROM tabl",
            source={
                "snowflake": "SELECT iff(col1) AS iff_col1 FROM tabl;",
            },
        )


def test_lower(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `lower` conversion of column
    validate_source_transpile(
        "SELECT LOWER(col1) AS lower_col1 FROM tabl",
        source={
            "snowflake": "SELECT lower(col1) AS lower_col1 FROM tabl;",
        },
    )

    # [TODO]
    # Snowflake also takes an optional rounding mode argument.
    # Need to handle in transpiler using round and bround function based on the mode.


def test_round(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `round` conversion of column
    validate_source_transpile(
        "SELECT ROUND(col1) AS round_col1 FROM tabl",
        source={
            "snowflake": "SELECT round(col1) AS round_col1 FROM tabl;",
        },
    )


def test_avg(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `avg` conversion of column
    validate_source_transpile(
        "SELECT AVG(col1) AS avg_col1 FROM tabl",
        source={
            "snowflake": "SELECT avg(col1) AS avg_col1 FROM tabl;",
        },
    )


def test_row_number(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `row_number` conversion of column
    validate_source_transpile(
        "SELECT symbol, exchange, shares, ROW_NUMBER() OVER (PARTITION BY exchange) AS row_number FROM trades",
        source={
            "snowflake": "SELECT symbol, exchange, shares, ROW_NUMBER() OVER (PARTITION BY exchange) AS "
            "row_number FROM trades;",
        },
    )


def test_ifnull(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `ifnull` conversion of column with two expressions
    validate_source_transpile(
        "SELECT COALESCE(col1, 'NA') AS ifnull_col1 FROM tabl",
        source={
            "snowflake": "SELECT ifnull(col1, 'NA') AS ifnull_col1 FROM tabl;",
        },
    )
    # Test case to validate `ifnull` conversion of single column:
    validate_source_transpile(
        "SELECT COALESCE(col1) AS ifnull_col1 FROM tabl",
        source={
            "snowflake": "SELECT ifnull(col1) AS ifnull_col1 FROM tabl;",
        },
    )


def test_current_date(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `current_date` conversion of column
    validate_source_transpile(
        "SELECT CURRENT_DATE FROM tabl",
        source={
            "snowflake": "SELECT current_date() FROM tabl;",
        },
    )


def test_upper(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `upper` conversion of column
    validate_source_transpile(
        "SELECT UPPER(col1) AS upper_col1 FROM tabl",
        source={
            "snowflake": "SELECT upper(col1) AS upper_col1 FROM tabl;",
        },
    )


def test_trim(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `trim` conversion of column
    # [TODO]
    # Both Databricks and Snowflake can take an optional set of characters to be trimmed as parameter.
    # Need to handle that case.
    validate_source_transpile(
        "SELECT TRIM(col1) AS trim_col1 FROM tabl",
        source={
            "snowflake": "SELECT trim(col1) AS trim_col1 FROM tabl;",
        },
    )

    # [TODO]
    # Date or time parts used in Snowflake differ from the ones used in Databricks. Need to handle this case.


def test_extract(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `extract` conversion of column
    validate_source_transpile(
        "SELECT EXTRACT(week FROM col1) AS extract_col1 FROM tabl",
        source={
            "snowflake": "SELECT extract(week FROM col1) AS extract_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `extract` conversion of column: ParseError
        # field and source are needed: `extract(field FROM source)`
        validate_source_transpile(
            "SELECT EXTRACT(col1) AS extract_col1 FROM tabl",
            source={
                "snowflake": "SELECT extract(col1) AS extract_col1 FROM tabl;",
            },
        )

    # [TODO]
    # Snowflake can take an optional time precision argument. Need to handle this case in Databricks.


def test_current_timestamp(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `current_timestamp` conversion of column
    validate_source_transpile(
        "SELECT CURRENT_TIMESTAMP() AS current_timestamp_col1 FROM tabl",
        source={
            "snowflake": "SELECT current_timestamp(col1) AS current_timestamp_col1 FROM tabl;",
        },
    )


def test_any_value(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `any_value` conversion of column
    validate_source_transpile(
        "SELECT customer.id, ANY_VALUE(customer.name), SUM(orders.value) FROM customer JOIN orders ON customer.id "
        "= orders.customer_id GROUP BY customer.id",
        source={
            "snowflake": "SELECT customer.id , ANY_VALUE(customer.name) , SUM(orders.value) FROM customer JOIN "
            "orders ON customer.id = orders.customer_id GROUP BY customer.id;",
        },
    )


def test_join(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `any_value` conversion of column
    validate_source_transpile(
        "SELECT t1.c1, t2.c2 FROM t1 JOIN t2 USING (c3)",
        source={
            "snowflake": "SELECT t1.c1, t2.c2 FROM t1 JOIN t2 USING (c3)",
        },
    )

    validate_source_transpile(
        "SELECT * FROM table1, table2 WHERE table1.column_name = table2.column_name",
        source={
            "snowflake": "SELECT * FROM table1, table2 WHERE table1.column_name = table2.column_name",
        },
    )


def test_try_cast(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `try_cast` conversion of static string
    validate_source_transpile(
        "SELECT TRY_CAST('10' AS DECIMAL(38, 0))",
        source={
            "snowflake": "SELECT try_cast('10' AS INT);",
        },
    )
    # Test case to validate `try_cast` conversion of column
    validate_source_transpile(
        "SELECT TRY_CAST(col1 AS DOUBLE) AS try_cast_col1 FROM tabl",
        source={
            "snowflake": "SELECT try_cast(col1 AS FLOAT) AS try_cast_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `try_cast` conversion of column: ParseError
        # sourceExpr and targetType are mandatory: try_cast(sourceExpr AS targetType)
        validate_source_transpile(
            "SELECT TRY_CAST(col1) AS try_cast_col1 FROM tabl",
            source={
                "snowflake": "SELECT try_cast(col1) AS try_cast_col1 FROM tabl;",
            },
        )


def test_abs(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `abs` conversion of column
    validate_source_transpile(
        "SELECT ABS(col1) AS abs_col1 FROM tabl",
        source={
            "snowflake": "SELECT abs(col1) AS abs_col1 FROM tabl;",
        },
    )


def test_replace(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `replace` conversion of column
    validate_source_transpile(
        "SELECT REPLACE('ABC_abc', 'abc', 'DEF')",
        source={
            "snowflake": "SELECT replace('ABC_abc', 'abc', 'DEF');",
        },
    )

    # [TODO]
    # In Snowflake, this function is overloaded; it can also be used as a numeric function to round down numeric
    # expressions. Also, it can take data time parts which are not supported in Databricks TRUNC function.
    # It may be transpiled to DATE_TRUNK function in Databricks.


def test_trunc(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `trunc` conversion of column
    validate_source_transpile(
        databricks_sql="SELECT TRUNC(col1, 'YEAR') AS trunc_col1 FROM tabl",
        source={
            "snowflake": "SELECT trunc(col1, 'YEAR') AS trunc_col1 FROM tabl;",
        },
    )
    with pytest.raises(UnsupportedError):
        # Test case to validate `trunc` conversion error:
        # UNIT is a mandatory argument: `trunc(expr, unit)`
        validate_source_transpile(
            "SELECT TRUNC(col1) AS trunc_col1 FROM tabl",
            source={
                "snowflake": "SELECT trunc(col1) AS trunc_col1 FROM tabl;",
            },
        )


def test_lag(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `lag` conversion of column
    validate_source_transpile(
        "SELECT LAG(col1) AS lag_col1 FROM tabl",
        source={
            "snowflake": "SELECT lag(col1) AS lag_col1 FROM tabl;",
        },
    )

    # [TODO]
    # In Snowflake replacement argument is optional and the default is an empty string
    # Also, occurrence and parameters arguments are not supported in Databricks
    # Need to handle these cases.


def test_regexp_replace(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `regexp_replace` conversion of column
    validate_source_transpile(
        "SELECT REGEXP_REPLACE(col1, '(\\d+)', '***') AS regexp_replace_col1 FROM tabl",
        source={
            "snowflake": "SELECT regexp_replace(col1, '(\\d+)', '***') AS regexp_replace_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `regexp_replace` conversion of column: ParseError
        # `str, regexp, rep` are mandatory. `position` is Optional
        # `regexp_replace(str, regexp, rep [, position] )`
        validate_source_transpile(
            "SELECT REGEXP_REPLACE(col1) AS regexp_replace_col1 FROM tabl",
            source={
                "snowflake": "SELECT regexp_replace(col1) AS regexp_replace_col1 FROM tabl;",
            },
        )


def test_greatest(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `greatest` conversion of column
    validate_source_transpile(
        "SELECT GREATEST(col_1, col_2, col_3) AS greatest_col1 FROM tabl",
        source={
            "snowflake": "SELECT greatest(col_1, col_2, col_3) AS greatest_col1 FROM tabl;",
        },
    )


def test_floor(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `floor` conversion of column
    validate_source_transpile(
        "SELECT FLOOR(col1) AS floor_col1 FROM tabl",
        source={
            "snowflake": "SELECT floor(col1) AS floor_col1 FROM tabl;",
        },
    )


def test_least(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `least` conversion of column
    validate_source_transpile(
        "SELECT LEAST(col1) AS least_col1 FROM tabl",
        source={
            "snowflake": "SELECT least(col1) AS least_col1 FROM tabl;",
        },
    )

    # [TODO]
    # DATE_PART in Snowflake can take various field names. Need to handle these cases.


def test_date_part(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `date_part` conversion of column
    validate_source_transpile(
        "SELECT EXTRACT(second FROM col1) AS date_part_col1 FROM tabl",
        source={
            "snowflake": "SELECT date_part('seconds', col1) AS date_part_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `date_part` conversion of column: ParseError
        # fieldStr, expr are mandatory: `date_part(fieldStr, expr)`
        validate_source_transpile(
            "SELECT DATE_PART(col1) AS date_part_col1 FROM tabl",
            source={
                "snowflake": "SELECT date_part(col1) AS date_part_col1 FROM tabl;",
            },
        )

    # [TODO]
    # Databricks doesn't take the optional date_part argument. Handle the case.


def test_last_day(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `last_day` conversion of column
    validate_source_transpile(
        "SELECT LAST_DAY(col1) AS last_day_col1 FROM tabl",
        source={
            "snowflake": "SELECT last_day(col1) AS last_day_col1 FROM tabl;",
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


def test_flatten(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `flatten` conversion of column
    validate_source_transpile(
        "SELECT EXPLODE(col1) AS flatten_col1 FROM tabl",
        source={
            "snowflake": "SELECT flatten(col1) AS flatten_col1 FROM tabl;",
        },
    )


def test_left(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `left` conversion of column
    validate_source_transpile(
        "SELECT LEFT(col1, 3) AS left_col1 FROM tabl",
        source={
            "snowflake": "SELECT left(col1, 3) AS left_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `left` conversion of column: ParseError
        # str, len both are needed: `left(str, len)`
        validate_source_transpile(
            "SELECT LEFT(col1) AS left_col1 FROM tabl",
            source={
                "snowflake": "SELECT left(col1) AS left_col1 FROM tabl;",
            },
        )


def test_sqrt(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `sqrt` conversion of column
    validate_source_transpile(
        "SELECT SQRT(col1) AS sqrt_col1 FROM tabl",
        source={
            "snowflake": "SELECT sqrt(col1) AS sqrt_col1 FROM tabl;",
        },
    )


def test_lead(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `lead` conversion of column
    validate_source_transpile(
        "SELECT LEAD(col1) AS lead_col1 FROM tabl",
        source={
            "snowflake": "SELECT lead(col1) AS lead_col1 FROM tabl;",
        },
    )


def test_percentile_disc(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `percentile_disc` conversion of column
    validate_source_transpile(
        "SELECT PERCENTILE_DISC(col1) AS percentile_disc_col1 FROM tabl",
        source={
            "snowflake": "SELECT percentile_disc(col1) AS percentile_disc_col1 FROM tabl;",
        },
    )

    # [TODO]
    # REGEXP_SUBSTR in Snowflake takes various parameters some of which are not supported in Databricks' REGEXP_EXTRACT
    # function. Need to handle this case.


def test_regexp_substr(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `regexp_substr` conversion of column
    validate_source_transpile(
        "SELECT REGEXP_EXTRACT(col1, '(E|e)rror') AS regexp_substr_col1 FROM tabl",
        source={
            "snowflake": "SELECT regexp_substr(col1, '(E|e)rror') AS regexp_substr_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `regexp_substr` conversion of column: ParseError
        # str, regexp args are mandatory: `regexp_substr( str, regexp )`
        validate_source_transpile(
            "SELECT REGEXP_SUBSTR(col1) AS regexp_substr_col1 FROM tabl",
            source={
                "snowflake": "SELECT regexp_substr(col1) AS regexp_substr_col1 FROM tabl;",
            },
        )

    # [TODO]
    # The separator argument in Snowflake is a plain string. But in Databricks it is a regex
    # For example, in Snowflake, we can call SPLIT('127.0.0.1', '.') but in Databricks we need to call
    # SPLIT('127.0.0.1', '\\.')
    # Need to handle this case.
    #
    # def test_split(dialect_context):
    #     validate_source_transpile, _ = dialect_context
    #     # Test case to validate `split` conversion of column
    #     validate_source_transpile(
    #         "SELECT SPLIT(col1, '[|.]') AS split_col1 FROM tabl",
    #         source={
    #             "snowflake": "SELECT split(col1, '[|.]') AS split_col1 FROM tabl;",
    #         },
    #     )
    #     with pytest.raises(ParseError):
    #         # Test case to validate `split` conversion of column: ParseError
    #         # str, regexp are mandatory. limit is Optional: `split(str, regex [, limit] )`
    #         validate_source_transpile(
    #             "SELECT SPLIT(col1) AS split_col1 FROM tabl",
    #             source={
    #                 "snowflake": "SELECT split(col1) AS split_col1 FROM tabl;",
    #             },
    #         )


def test_rank(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `rank` conversion of column
    validate_source_transpile(
        "SELECT RANK(col1) AS rank_col1 FROM tabl",
        source={
            "snowflake": "SELECT rank(col1) AS rank_col1 FROM tabl;",
        },
    )


def test_contains(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `contains` conversion of column
    validate_source_transpile(
        "SELECT CONTAINS('SparkSQL', 'Spark')",
        source={
            "snowflake": "SELECT contains('SparkSQL', 'Spark');",
        },
    )


def test_last_value(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `last_value` conversion of column
    validate_source_transpile(
        "SELECT LAST_VALUE(col1) AS last_value_col1 FROM tabl",
        source={
            "snowflake": "SELECT last_value(col1) AS last_value_col1 FROM tabl;",
        },
    )


def test_lpad(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `lpad` conversion of column
    validate_source_transpile(
        "SELECT LPAD('hi', 5, 'ab')",
        source={
            "snowflake": "SELECT lpad('hi', 5, 'ab');",
        },
    )

    # [TODO]
    # The syntax POSITION( <expr1> IN <expr2> ) is not supported in locate. The transpiler converts position to locate.
    # There is a native position function in Databricks. We can use that. Needs to be handled.


def test_position(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `position` conversion of column `position(substr, str [, pos] )`
    validate_source_transpile(
        "SELECT LOCATE('exc', col1) AS position_col1 FROM tabl",
        source={
            "snowflake": "SELECT position('exc', col1) AS position_col1 FROM tabl;",
        },
    )
    # # Test case to validate `position` conversion of column `position(subtr IN str)`
    # validate_source_transpile(
    #     "SELECT LOCATE('exc' IN col1) AS position_col1 FROM tabl",
    #     source={
    #         "snowflake": "SELECT position('exc' IN col1) AS position_col1 FROM tabl;",
    #     },
    # )
    with pytest.raises(ParseError):
        # Test case to validate `position` conversion of column: ParseError
        # substr, str are mandatory, pos is Optional: `position(substr, str [, pos] )` or  `position(subtr IN str)`
        validate_source_transpile(
            "SELECT POSITION(col1) AS position_col1 FROM tabl",
            source={
                "snowflake": "SELECT position(col1) AS position_col1 FROM tabl;",
            },
        )


def test_equal_null(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `equal_null` conversion of column
    validate_source_transpile(
        "SELECT EQUAL_NULL(2, 2) AS equal_null_col1 FROM tabl",
        source={
            "snowflake": "SELECT equal_null(2, 2) AS equal_null_col1 FROM tabl;",
        },
    )


def test_right(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `right` conversion of column
    validate_source_transpile(
        "SELECT RIGHT(col1, 5) AS right_col1 FROM tabl",
        source={
            "snowflake": "SELECT right(col1, 5) AS right_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `right` conversion of column: ParseError
        # str, len both are needed: `right(str, len)`
        validate_source_transpile(
            "SELECT RIGHT(col1) AS left_col1 FROM tabl",
            source={
                "snowflake": "SELECT right(col1) AS left_col1 FROM tabl;",
            },
        )


def test_mode(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `mode` conversion of column
    validate_source_transpile(
        "SELECT MODE(col1) AS mode_col1 FROM tabl",
        source={
            "snowflake": "SELECT mode(col1) AS mode_col1 FROM tabl;",
        },
    )

    # [TODO]
    # Both Databricks and Snowflake can take an optional set of characters to be trimmed as parameter.
    # Need to handle that case.


def test_ltrim(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `ltrim` conversion of column
    validate_source_transpile(
        "SELECT LTRIM(col1) AS ltrim_col1 FROM tabl",
        source={
            "snowflake": "SELECT ltrim(col1) AS ltrim_col1 FROM tabl;",
        },
    )


def test_array_size(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `array_size` conversion of column
    validate_source_transpile(
        "SELECT SIZE(col1) AS array_size_col1 FROM tabl",
        source={
            "snowflake": "SELECT array_size(col1) AS array_size_col1 FROM tabl;",
        },
    )


def test_rpad(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `rpad` conversion of column
    validate_source_transpile(
        "SELECT RPAD('hi', 5, 'ab')",
        source={
            "snowflake": "SELECT rpad('hi', 5, 'ab');",
        },
    )


def test_first_value(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `first_value` conversion of column
    validate_source_transpile(
        "SELECT FIRST_VALUE(col1) AS first_value_col1 FROM tabl",
        source={
            "snowflake": "SELECT first_value(col1) AS first_value_col1 FROM tabl;",
        },
    )


def test_ntile(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `ntile` conversion of column
    validate_source_transpile(
        "SELECT NTILE(col1) AS ntile_col1 FROM tabl",
        source={
            "snowflake": "SELECT ntile(col1) AS ntile_col1 FROM tabl;",
        },
    )


def test_median(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `median` conversion of column
    validate_source_transpile(
        "SELECT MEDIAN(col1) AS median_col1 FROM tabl",
        source={
            "snowflake": "SELECT median(col1) AS median_col1 FROM tabl;",
        },
    )


def test_get(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `get` conversion of column
    validate_source_transpile(
        "SELECT GET(col1) AS get_col1 FROM tabl",
        source={
            "snowflake": "SELECT get(col1) AS get_col1 FROM tabl;",
        },
    )


def test_add_months(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `add_months` conversion of column
    validate_source_transpile(
        "SELECT ADD_MONTHS(col1, 1) AS add_months_col1 FROM tabl",
        source={
            "snowflake": "SELECT add_months(col1,1) AS add_months_col1 FROM tabl;",
        },
    )


def test_to_timestamp(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `to_timestamp` conversion of column
    validate_source_transpile(
        "SELECT to_timestamp(col1) AS to_timestamp_col1 FROM tabl",
        source={
            "snowflake": "SELECT to_timestamp(col1) AS to_timestamp_col1 FROM tabl;",
        },
    )


def test_array_contains(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `array_contains` conversion of column
    # The order of arguments is different in Databricks and Snowflake
    validate_source_transpile(
        "SELECT ARRAY_CONTAINS(arr_col, 33) AS array_contains_col1 FROM tabl",
        source={
            "snowflake": "SELECT array_contains(33, arr_col) AS array_contains_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `array_contains` conversion of column
        # array, value both are mandatory args: `array_contains(array, value)`
        validate_source_transpile(
            "SELECT ARRAY_CONTAINS(arr_col) AS array_contains_col1 FROM tabl",
            source={
                "snowflake": "SELECT array_contains(arr_col) AS array_contains_col1 FROM tabl;",
            },
        )


def test_percentile_cont(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `percentile_cont` conversion of column
    validate_source_transpile(
        "SELECT PERCENTILE_CONT(col1) AS percentile_cont_col1 FROM tabl",
        source={
            "snowflake": "SELECT percentile_cont(col1) AS percentile_cont_col1 FROM tabl;",
        },
    )


def test_percent_rank(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `percent_rank` conversion of column
    validate_source_transpile(
        "SELECT PERCENT_RANK() AS percent_rank_col1 FROM tabl",
        source={
            "snowflake": "SELECT percent_rank() AS percent_rank_col1 FROM tabl;",
        },
    )


def test_stddev(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `stddev` conversion of column
    validate_source_transpile(
        "SELECT STDDEV(col1) AS stddev_col1 FROM tabl",
        source={
            "snowflake": "SELECT stddev(col1) AS stddev_col1 FROM tabl;",
        },
    )


def test_hash(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `hash` conversion of column
    validate_source_transpile(
        "SELECT HASH(col1) AS hash_col1 FROM tabl",
        source={
            "snowflake": "SELECT hash(col1) AS hash_col1 FROM tabl;",
        },
    )


def test_arrays_overlap(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `arrays_overlap` conversion of column
    validate_source_transpile(
        "SELECT ARRAYS_OVERLAP(ARRAY(1, 2, NULL), ARRAY(3, NULL, 5))",
        source={
            "snowflake": "SELECT ARRAYS_OVERLAP(ARRAY_CONSTRUCT(1, 2, NULL), ARRAY_CONSTRUCT(3, NULL, 5));",
        },
    )


def test_dense_rank(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `dense_rank` conversion of column
    validate_source_transpile(
        "SELECT DENSE_RANK(col1) AS dense_rank_col1 FROM tabl",
        source={
            "snowflake": "SELECT dense_rank(col1) AS dense_rank_col1 FROM tabl;",
        },
    )

    # [TODO]
    # Snowflake can also take an optional argument delimiters.
    # Need to handle that, may be add a warning message if delimiter is present


def test_initcap(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `initcap` conversion of column
    validate_source_transpile(
        "SELECT INITCAP(col1) AS initcap_col1 FROM tabl",
        source={
            "snowflake": "SELECT initcap(col1) AS initcap_col1 FROM tabl;",
        },
    )


def test_mod(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `mod` conversion of column
    validate_source_transpile(
        "SELECT MOD(col1, col2) AS mod_col1 FROM tabl",
        source={
            "snowflake": "SELECT mod(col1, col2) AS mod_col1 FROM tabl;",
        },
    )


def test_count_if(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `count_if` conversion of column
    validate_source_transpile(
        "SELECT COUNT_IF(j_col > i_col) FROM basic_example",
        source={
            "snowflake": "SELECT COUNT_IF(j_col > i_col) FROM basic_example;",
        },
    )


def test_radians(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `radians` conversion of column
    validate_source_transpile(
        "SELECT RADIANS(col1) AS radians_col1 FROM tabl",
        source={
            "snowflake": "SELECT radians(col1) AS radians_col1 FROM tabl;",
        },
    )

    # [TODO]
    # Both Databricks and Snowflake can take an optional set of characters to be trimmed as parameter.
    # Need to handle that case.


def test_rtrim(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `rtrim` conversion of column
    validate_source_transpile(
        "SELECT RTRIM(col1) AS rtrim_col1 FROM tabl",
        source={
            "snowflake": "SELECT rtrim(col1) AS rtrim_col1 FROM tabl;",
        },
    )


def test_ceil(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `ceil` conversion of column
    validate_source_transpile(
        "SELECT CEIL(col1) AS ceil_col1 FROM tabl",
        source={
            "snowflake": "SELECT ceil(col1) AS ceil_col1 FROM tabl;",
        },
    )


def test_startswith(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `startswith` conversion of column
    validate_source_transpile(
        "SELECT STARTSWITH(col1, 'Spark') AS startswith_col1 FROM tabl",
        source={
            "snowflake": "SELECT startswith(col1, 'Spark') AS startswith_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `startswith` conversion of column: ParseError
        # expr, startExpr both args are mandatory: `startswith(expr, startExpr)`
        validate_source_transpile(
            "SELECT STARTSWITH(col1) AS startswith_col1 FROM tabl",
            source={
                "snowflake": "SELECT startswith(col1) AS startswith_col1 FROM tabl;",
            },
        )

    # [TODO]
    # The regex format may differ between Snowflake and Databricks. Needs manual intervention.
    # Also Snowflake may take optional regex parameters.
    # We may put a warning message so that users can validate manually.


def test_regexp_like(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `regexp_like` conversion of column
    validate_source_transpile(
        "SELECT col1 RLIKE '\\Users.*' AS regexp_like_col1 FROM tabl",
        source={
            "snowflake": "SELECT regexp_like(col1, '\\Users.*') AS regexp_like_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `regexp_like` conversion of column
        # str, regex args are mandatory: `regexp_like( str, regex )`
        validate_source_transpile(
            "SELECT REGEXP_LIKE(col1) AS regexp_like_col1 FROM tabl",
            source={
                "snowflake": "SELECT regexp_like(col1) AS regexp_like_col1 FROM tabl;",
            },
        )

    # [TODO]
    # Behavior of PARSE_URL is different in Snowflake and Databricks.
    # Need to handle it accordingly.


def test_parse_url(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `parse_url` conversion of column
    validate_source_transpile(
        "SELECT PARSE_URL(col1) AS parse_url_col1 FROM tabl",
        source={
            "snowflake": "SELECT parse_url(col1) AS parse_url_col1 FROM tabl;",
        },
    )

    # [TODO]
    # Currently the transpiler converts the decode function to CASE.
    # Databricks has native decode function which behaves like the same function in Snowflake.
    # We can use that instead.


def test_decode(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `decode` conversion of column
    validate_source_transpile(
        "SELECT CASE WHEN column1 = 1 THEN 'one' WHEN column1 = 2 THEN 'two' WHEN column1 IS NULL THEN '-NULL-' "
        "ELSE 'other' END AS decode_result",
        source={
            "snowflake": "SELECT decode(column1, 1, 'one', 2, 'two', NULL, '-NULL-', 'other') AS decode_result;",
        },
    )


def test_exp(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `exp` conversion of column
    validate_source_transpile(
        "SELECT EXP(col1) AS exp_col1 FROM tabl",
        source={
            "snowflake": "SELECT exp(col1) AS exp_col1 FROM tabl;",
        },
    )


def test_reverse(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `reverse` conversion of column
    validate_source_transpile(
        "SELECT REVERSE(col1) AS reverse_col1 FROM tabl",
        source={
            "snowflake": "SELECT reverse(col1) AS reverse_col1 FROM tabl;",
        },
    )


def test_ln(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `ln` conversion of column
    validate_source_transpile(
        "SELECT LN(col1) AS ln_col1 FROM tabl",
        source={
            "snowflake": "SELECT ln(col1) AS ln_col1 FROM tabl;",
        },
    )


def test_cos(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `cos` conversion of column
    validate_source_transpile(
        "SELECT COS(col1) AS cos_col1 FROM tabl",
        source={
            "snowflake": "SELECT cos(col1) AS cos_col1 FROM tabl;",
        },
    )


def test_endswith(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `endswith` conversion of column
    validate_source_transpile(
        "SELECT ENDSWITH('SparkSQL', 'SQL')",
        source={
            "snowflake": "SELECT endswith('SparkSQL', 'SQL');",
        },
    )


def test_random(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `random` conversion of column
    validate_source_transpile(
        "SELECT RANDOM(), RANDOM(col1) FROM tabl",
        source={
            "snowflake": "SELECT random(), random(col1) FROM tabl;",
        },
    )


def test_sign(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `sign` conversion of column
    validate_source_transpile(
        "SELECT SIGN(col1) AS sign_col1 FROM tabl",
        source={
            "snowflake": "SELECT sign(col1) AS sign_col1 FROM tabl;",
        },
    )


def test_sin(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `sin` conversion of column
    validate_source_transpile(
        "SELECT SIN(col1) AS sin_col1 FROM tabl",
        source={
            "snowflake": "SELECT sin(col1) AS sin_col1 FROM tabl;",
        },
    )


def test_to_json(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `to_json` conversion of column
    validate_source_transpile(
        "SELECT TO_JSON(col1) AS to_json_col1 FROM tabl",
        source={
            "snowflake": "SELECT to_json(col1) AS to_json_col1 FROM tabl;",
        },
    )


def test_concat_ws(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `concat_ws` conversion of column
    validate_source_transpile(
        "SELECT CONCAT_WS(',', 'one', 'two', 'three')",
        source={
            "snowflake": "SELECT CONCAT_WS(',', 'one', 'two', 'three');",
        },
    )


def test_array_prepend(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `array_prepend` conversion of column
    validate_source_transpile(
        "SELECT ARRAY_PREPEND(array, elem) AS array_prepend_col1 FROM tabl",
        source={
            "snowflake": "SELECT array_prepend(array, elem) AS array_prepend_col1 FROM tabl;",
        },
    )


def test_stddev_pop(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `stddev_pop` conversion of column
    validate_source_transpile(
        "SELECT STDDEV_POP(col1) AS stddev_pop_col1 FROM tabl",
        source={
            "snowflake": "SELECT stddev_pop(col1) AS stddev_pop_col1 FROM tabl;",
        },
    )

    # [TODO]
    # Snowflake version takes optional parameters.
    # Show warning message if applicable.


def test_regexp_count(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `regexp_count` conversion of column
    validate_source_transpile(
        "SELECT REGEXP_COUNT(col1) AS regexp_count_col1 FROM tabl",
        source={
            "snowflake": "SELECT regexp_count(col1) AS regexp_count_col1 FROM tabl;",
        },
    )


def test_log(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `log` conversion of column
    validate_source_transpile(
        "SELECT LOG(x, y) AS log_col1 FROM tabl",
        source={
            "snowflake": "SELECT log(x, y) AS log_col1 FROM tabl;",
        },
    )


def test_approx_percentile(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `approx_percentile` conversion of column
    validate_source_transpile(
        "SELECT APPROX_PERCENTILE(col1, 0.5) AS approx_percentile_col1 FROM tabl",
        source={
            "snowflake": "SELECT approx_percentile(col1, 0.5) AS approx_percentile_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `approx_percentile` conversion of column: ParseError
        # expr, percentile are mandatory. accuracy, cond are optional
        # `approx_percentile ( [ALL | DISTINCT] expr, percentile [, accuracy] ) [ FILTER ( WHERE cond ) ]`
        validate_source_transpile(
            "SELECT APPROX_PERCENTILE(col1) AS approx_percentile_col1 FROM tabl",
            source={
                "snowflake": "SELECT approx_percentile(col1) AS approx_percentile_col1 FROM tabl;",
            },
        )


def test_array_distinct(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `array_distinct` conversion of column
    validate_source_transpile(
        "SELECT ARRAY_DISTINCT(col1) AS array_distinct_col1 FROM tabl",
        source={
            "snowflake": "SELECT array_distinct(col1) AS array_distinct_col1 FROM tabl;",
        },
    )


def test_array_compact(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `array_compact` conversion of column
    validate_source_transpile(
        "SELECT ARRAY_COMPACT(col1) AS array_compact_col1 FROM tabl",
        source={
            "snowflake": "SELECT array_compact(col1) AS array_compact_col1 FROM tabl;",
        },
    )


def test_corr(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `corr` conversion of column
    validate_source_transpile(
        "SELECT CORR(v, v2) AS corr_col1 FROM tabl",
        source={
            "snowflake": "SELECT CORR(v, v2) AS corr_col1 FROM tabl;",
        },
    )

    # [TODO]
    # Snowflake version takes optional arguments.
    # Need to handle with a warning message if those arguments are passed.


def test_regexp_instr(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `regexp_instr` conversion of column
    validate_source_transpile(
        "SELECT REGEXP_INSTR(col1) AS regexp_instr_col1 FROM tabl",
        source={
            "snowflake": "SELECT regexp_instr(col1) AS regexp_instr_col1 FROM tabl;",
        },
    )


def test_repeat(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `repeat` conversion of column
    validate_source_transpile(
        "SELECT REPEAT(col1, 5) AS repeat_col1 FROM tabl",
        source={
            "snowflake": "SELECT repeat(col1, 5) AS repeat_col1 FROM tabl;",
        },
    )

    with pytest.raises(ParseError):
        validate_source_transpile, _ = dialect_context
        # Test case to validate `repeat` conversion of column: ParseError
        # expr, n times both are needed:  `repeat(expr, n)`
        validate_source_transpile(
            "SELECT REPEAT(col1) AS repeat_col1 FROM tabl",
            source={
                "snowflake": "SELECT repeat(col1) AS repeat_col1 FROM tabl;",
            },
        )


def test_nvl2(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `nvl2` conversion of static expressions
    validate_source_transpile(
        "SELECT NVL2(NULL, 2, 1)",
        source={
            "snowflake": "SELECT nvl2(NULL, 2, 1);",
        },
    )
    # Test case to validate `nvl2` conversion of column
    validate_source_transpile(
        "SELECT NVL2(cond, col1, col2) AS nvl2_col1 FROM tabl",
        source={
            "snowflake": "SELECT nvl2(cond, col1, col2) AS nvl2_col1 FROM tabl;",
        },
    )
    with pytest.raises(ParseError):
        # Test case to validate `nvl2` conversion of column: ParseError
        # 3 arguments are needed: `nvl2(expr1, expr2, expr3)`
        validate_source_transpile(
            "SELECT NVL2(col1) AS nvl2_col1 FROM tabl",
            source={
                "snowflake": "SELECT nvl2(col1) AS nvl2_col1 FROM tabl;",
            },
        )


def test_asin(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `asin` conversion of column
    validate_source_transpile(
        "SELECT ASIN(col1) AS asin_col1 FROM tabl",
        source={
            "snowflake": "SELECT asin(col1) AS asin_col1 FROM tabl;",
        },
    )


def test_pi(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `pi` conversion of column
    validate_source_transpile(
        "SELECT PI() AS pi_col1 FROM tabl",
        source={
            "snowflake": "SELECT PI() AS pi_col1 FROM tabl;",
        },
    )


def test_stddev_samp(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `stddev_samp` conversion of column
    validate_source_transpile(
        "SELECT STDDEV_SAMP(col1) AS stddev_samp_col1 FROM tabl",
        source={
            "snowflake": "SELECT stddev_samp(col1) AS stddev_samp_col1 FROM tabl;",
        },
    )


def test_tan(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `tan` conversion of column
    validate_source_transpile(
        "SELECT TAN(col1) AS tan_col1 FROM tabl",
        source={
            "snowflake": "SELECT tan(col1) AS tan_col1 FROM tabl;",
        },
    )

    # [TODO]
    # Default argument values are different in Snowflake and Databricks
    # Need to handle these cases.


def test_approx_top_k(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `approx_top_k` conversion of column
    validate_source_transpile(
        "SELECT APPROX_TOP_K(col1) AS approx_top_k_col1 FROM tabl",
        source={
            "snowflake": "SELECT approx_top_k(col1) AS approx_top_k_col1 FROM tabl;",
        },
    )


def test_next_day(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `next_day` conversion of column
    validate_source_transpile(
        "SELECT NEXT_DAY('2015-01-14', 'TU') AS next_day_col1 FROM tabl",
        source={
            "snowflake": "SELECT next_day('2015-01-14', 'TU') AS next_day_col1 FROM tabl;",
        },
    )


def test_regr_intercept(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `regr_intercept` conversion of column
    validate_source_transpile(
        "SELECT REGR_INTERCEPT(v, v2) AS regr_intercept_col1 FROM tabl",
        source={
            "snowflake": "SELECT regr_intercept(v, v2) AS regr_intercept_col1 FROM tabl;",
        },
    )


def test_regr_r2(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `regr_r2` conversion of column
    validate_source_transpile(
        "SELECT REGR_R2(v, v2) AS regr_r2_col1 FROM tabl",
        source={
            "snowflake": "SELECT regr_r2(v, v2) AS regr_r2_col1 FROM tabl;",
        },
    )


def test_regr_slope(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `regr_slope` conversion of column
    validate_source_transpile(
        "SELECT REGR_SLOPE(v, v2) AS regr_slope_col1 FROM tabl",
        source={
            "snowflake": "SELECT regr_slope(v, v2) AS regr_slope_col1 FROM tabl;",
        },
    )


def test_cume_dist(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `cume_dist` conversion of column
    validate_source_transpile(
        "SELECT CUME_DIST() AS cume_dist_col1 FROM tabl",
        source={
            "snowflake": "SELECT cume_dist() AS cume_dist_col1 FROM tabl;",
        },
    )


def test_translate(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `translate` conversion of column
    validate_source_transpile(
        "SELECT TRANSLATE('AaBbCc', 'abc', '123') AS translate_col1 FROM tabl",
        source={
            "snowflake": "SELECT translate('AaBbCc', 'abc', '123') AS translate_col1 FROM tabl;",
        },
    )


def test_typeof(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `typeof` conversion of column
    validate_source_transpile(
        "SELECT TYPEOF(col1) AS typeof_col1 FROM tabl",
        source={
            "snowflake": "SELECT typeof(col1) AS typeof_col1 FROM tabl;",
        },
    )


def test_array_except(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `array_except` conversion of column
    validate_source_transpile(
        "SELECT ARRAY_EXCEPT(a, b) AS array_except_col1 FROM tabl",
        source={
            "snowflake": "SELECT array_except(a, b) AS array_except_col1 FROM tabl;",
        },
    )


def test_current_database(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `current_database` conversion of column
    validate_source_transpile(
        "SELECT CURRENT_DATABASE() AS current_database_col1 FROM tabl",
        source={
            "snowflake": "SELECT current_database() AS current_database_col1 FROM tabl;",
        },
    )


def test_array_append(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `array_append` conversion of column
    validate_source_transpile(
        "SELECT ARRAY_APPEND(array, elem) AS array_append_col1 FROM tabl",
        source={
            "snowflake": "SELECT array_append(array, elem) AS array_append_col1 FROM tabl;",
        },
    )

    # [TODO]
    # In Snowflake and Databricks the positions of the arguments are interchanged.
    # Needs to be handled in the transpiler.


def test_array_position(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `array_position` conversion of column
    validate_source_transpile(
        "SELECT ARRAY_POSITION(col1) AS array_position_col1 FROM tabl",
        source={
            "snowflake": "SELECT array_position(col1) AS array_position_col1 FROM tabl;",
        },
    )


def test_array_remove(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `array_remove` conversion of column
    validate_source_transpile(
        "SELECT ARRAY_REMOVE(array, element) AS array_remove_col1 FROM tabl",
        source={
            "snowflake": "SELECT array_remove(array, element) AS array_remove_col1 FROM tabl;",
        },
    )


def test_atan2(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `atan2` conversion of column
    validate_source_transpile(
        "SELECT ATAN2(exprY, exprX) AS atan2_col1 FROM tabl",
        source={
            "snowflake": "SELECT atan2(exprY, exprX) AS atan2_col1 FROM tabl;",
        },
    )

    # [TODO]
    # Snowflake supports FROM { FIRST | LAST }
    # Need to handle this if FROM LAST is used in the query


def test_nth_value(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `nth_value` conversion of column
    validate_source_transpile(
        "SELECT NTH_VALUE(col1) AS nth_value_col1 FROM tabl",
        source={
            "snowflake": "SELECT nth_value(col1) AS nth_value_col1 FROM tabl;",
        },
    )


def test_parse_json(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `parse_json` conversion of column
    validate_source_transpile(
        "SELECT tt.id, FROM_JSON(tt.details, {TT.DETAILS_SCHEMA}) FROM prod.public.table AS tt",
        source={
            "snowflake": "SELECT tt.id, PARSE_JSON(tt.details) FROM prod.public.table tt;",
        },
    )
    # Test case to validate `parse_json` conversion of column
    validate_source_transpile(
        "SELECT col1, FROM_JSON(col2, {COL2_SCHEMA}) FROM tabl",
        source={
            "snowflake": "SELECT col1, TRY_PARSE_JSON(col2) FROM tabl;",
        },
    )


def test_dayname(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `dayname` parsing of timestamp column
    validate_source_transpile(
        """SELECT DATE_FORMAT(cast('2015-04-03 10:00:00' as timestamp), 'E') AS MONTH""",
        source={
            "snowflake": """SELECT DAYNAME(TO_TIMESTAMP('2015-04-03 10:00:00')) AS MONTH;""",
        },
    )
    # Test case to validate `dayname` parsing of date column
    validate_source_transpile(
        """SELECT DATE_FORMAT(cast('2015-05-01' as date), 'E') AS MONTH""",
        source={
            "snowflake": """SELECT DAYNAME(TO_DATE('2015-05-01')) AS MONTH;""",
        },
    )
    # Test case to validate `dayname` parsing of string column with hours and minutes
    validate_source_transpile(
        """SELECT DATE_FORMAT('2015-04-03 10:00', 'E') AS MONTH""",
        source={
            "snowflake": """SELECT DAYNAME('2015-04-03 10:00') AS MONTH;""",
        },
    )

    with pytest.raises(ParseError):
        validate_source_transpile(
            """SELECT DATE_FORMAT('2015-04-03 10:00', 'E') AS MONTH""",
            source={
                "snowflake": """SELECT DAYNAME('2015-04-03 10:00', 'EEE') AS MONTH;""",
            },
        )


def test_to_number(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `TO_DECIMAL` parsing with format
    validate_source_transpile(
        """SELECT TO_NUMBER('$345', '$999.00') AS col1""",
        source={
            "snowflake": """SELECT TO_DECIMAL('$345', '$999.00') AS col1""",
        },
    )
    # Test case to validate `TO_NUMERIC` parsing with format
    validate_source_transpile(
        """SELECT TO_NUMBER('$345', '$999.99') AS num""",
        source={
            "snowflake": """SELECT TO_NUMERIC('$345', '$999.99') AS num""",
        },
    )
    # Test case to validate `TO_NUMBER` parsing with format
    validate_source_transpile(
        """SELECT TO_NUMBER('$345', '$999.99') AS num""",
        source={
            "snowflake": """SELECT TO_NUMBER('$345', '$999.99') AS num""",
        },
    )
    # Test case to validate `TO_DECIMAL`, `TO_NUMERIC` parsing with format from table columns
    validate_source_transpile(
        """SELECT TO_NUMBER(col1, '$999.099'),
        TO_NUMBER(tbl.col2, '$999,099.99') FROM dummy AS tbl""",
        source={
            "snowflake": """SELECT TO_DECIMAL(col1, '$999.099'),
                TO_NUMERIC(tbl.col2, '$999,099.99') FROM dummy tbl""",
        },
    )
    # Test case to validate `TO_NUMERIC` parsing with format, precision and scale from static string
    validate_source_transpile(
        """SELECT CAST(TO_NUMBER('$345', '$999.99') AS DECIMAL(5, 2)) AS num_with_scale""",
        source={
            "snowflake": """SELECT TO_NUMERIC('$345', '$999.99', 5, 2) AS num_with_scale""",
        },
    )
    # Test case to validate `TO_DECIMAL` parsing with format, precision and scale from static string
    validate_source_transpile(
        """SELECT CAST(TO_NUMBER('$755', '$999.00') AS DECIMAL(15, 5)) AS num_with_scale""",
        source={
            "snowflake": """SELECT TO_DECIMAL('$755', '$999.00', 15, 5) AS num_with_scale""",
        },
    )
    # Test case to validate `TO_NUMERIC`, `TO_NUMBER` parsing with format, precision and scale from table columns
    validate_source_transpile(
        """SELECT CAST(TO_NUMBER(sm.col1, '$999.00') AS DECIMAL(15, 5)) AS col1,
        CAST(TO_NUMBER(sm.col2, '$99.00') AS DECIMAL(15, 5)) AS col2 FROM sales_reports AS sm""",
        source={
            "snowflake": """SELECT TO_NUMERIC(sm.col1, '$999.00', 15, 5) AS col1,
                TO_NUMBER(sm.col2, '$99.00', 15, 5) AS col2 FROM sales_reports sm""",
        },
    )

    # Test case to validate `TO_NUMBER` parsing with precision and scale from table columns.
    validate_source_transpile(
        """SELECT CAST(col1 AS DECIMAL(15, 5)) AS col1 FROM sales_reports""",
        source={
            "snowflake": """SELECT TO_NUMERIC(col1, 15, 5) AS col1 FROM sales_reports""",
        },
    )

    with pytest.raises(UnsupportedError):
        # Test case to validate `TO_DECIMAL` parsing without format
        validate_source_transpile(
            """SELECT CAST(TO_NUMBER('$345', '$999.00') AS DECIMAL(38, 0)) AS col1""",
            source={
                "snowflake": """SELECT TO_DECIMAL('$345') AS col1""",
            },
        )

    with pytest.raises(ParseError):
        validate_source_transpile(
            """SELECT CAST(TO_NUMBER('$345', '$999.99') AS DECIMAL(5, 2)) AS num_with_scale""",
            source={
                "snowflake": """SELECT TO_NUMERIC('$345', '$999.99', 5, 2, 1) AS num_with_scale""",
            },
        )


def test_to_time(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test case to validate `TRY_TO_DATE` parsing with default format
    validate_source_transpile(
        """SELECT TO_TIMESTAMP('2018-05-15', 'yyyy-MM-d')""",
        source={
            "snowflake": """SELECT TO_TIME('2018-05-15', 'yyyy-MM-dd')""",
        },
    )
    # Test case to validate `TRY_TO_DATE` parsing with default format
    validate_source_transpile(
        """SELECT TO_TIMESTAMP('2018-05-15 00:01:02', 'yyyy-MM-dd HH:mm:ss')""",
        source={
            "snowflake": """SELECT TO_TIME('2018-05-15 00:01:02')""",
        },
    )


def test_timestamp_from_parts(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        """SELECT MAKE_TIMESTAMP(1992, 6, 1, 12, 35, 12)""",
        source={
            "snowflake": """select timestamp_from_parts(1992, 6, 1, 12, 35, 12);""",
        },
    )
    validate_source_transpile(
        """SELECT MAKE_TIMESTAMP(2023, 10, 3, 14, 10, 45), MAKE_TIMESTAMP(2020, 4, 4, 4, 5, 6)""",
        source={
            "snowflake": """select TIMESTAMP_FROM_PARTS(2023, 10, 3, 14, 10, 45),
                timestamp_from_parts(2020, 4, 4, 4, 5, 6);""",
        },
    )


def test_to_variant(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        """SELECT TO_JSON(col1) AS json_col1 FROM dummy""",
        source={
            "snowflake": """SELECT to_variant(col1) AS json_col1 FROM dummy;""",
        },
    )


def test_to_array(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        """SELECT IF(col1 IS NULL, NULL, ARRAY(col1)) AS ary_col""",
        source={
            "snowflake": """SELECT to_array(col1) AS ary_col;""",
        },
    )


def test_to_rlike(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        r"""SELECT '800-456-7891' RLIKE '[2-9]\d{2}-\d{3}-\d{4}' AS matches_phone_number""",
        source={
            "snowflake": """SELECT RLIKE('800-456-7891','[2-9]\\d{2}-\\d{3}-\\d{4}') AS matches_phone_number;;""",
        },
    )


def test_try_to_boolean(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
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
        source={
            "snowflake": "select TRY_TO_BOOLEAN(1);",
        },
    )


def test_sysdate(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()",
        source={
            "snowflake": """SELECT SYSDATE(), CURRENT_TIMESTAMP();""",
        },
    )


def test_booland_agg(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT BOOL_AND(k) FROM bool_example",
        source={
            "snowflake": "select booland_agg(k) from bool_example",
        },
    )
    validate_source_transpile(
        "SELECT s2, BOOL_AND(k) FROM bool_example GROUP BY s2",
        source={
            "snowflake": "select s2, booland_agg(k) from bool_example group by s2",
        },
    )


def test_base64_encode(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT BASE64('HELLO'), BASE64('HELLO')",
        source={
            "snowflake": "SELECT BASE64_ENCODE('HELLO'), BASE64_ENCODE('HELLO');",
        },
    )


def test_base64_decode(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT UNBASE64(BASE64('HELLO')), UNBASE64(BASE64('HELLO'))",
        source={
            "snowflake": "SELECT BASE64_DECODE_STRING(BASE64_ENCODE('HELLO')), "
            "TRY_BASE64_DECODE_STRING(BASE64_ENCODE('HELLO'));",
        },
    )


def test_array_construct_compact(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT ARRAY(NULL, 'hello', CAST(3 AS DOUBLE), 4, 5)",
        source={
            "snowflake": "SELECT ARRAY_CONSTRUCT(null, 'hello', 3::double, 4, 5);",
        },
    )
    validate_source_transpile(
        "SELECT ARRAY_EXCEPT(ARRAY(NULL, 'hello', CAST(3 AS DOUBLE), 4, 5), ARRAY(NULL))",
        source={
            "snowflake": "SELECT ARRAY_CONSTRUCT_COMPACT(null, 'hello', 3::double, 4, 5);",
        },
    )


def test_to_double(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT DOUBLE('HELLO')",
        source={
            "snowflake": "SELECT TO_DOUBLE('HELLO')",
        },
    )


def test_array_intersection(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT ARRAY_INTERSECT(col1, col2)",
        source={
            "snowflake": "SELECT ARRAY_INTERSECTION(col1, col2)",
        },
    )
    validate_source_transpile(
        "SELECT ARRAY_INTERSECT(ARRAY(1, 2, 3), ARRAY(1, 2))",
        source={
            "snowflake": "SELECT ARRAY_INTERSECTION(ARRAY_CONSTRUCT(1, 2, 3), ARRAY_CONSTRUCT(1, 2))",
        },
    )


def test_to_object(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "SELECT TO_JSON(k) FROM tabl",
        source={
            "snowflake": "SELECT to_object(k) FROM tabl",
        },
    )


def test_array_slice(dialect_context):
    validate_source_transpile, _ = dialect_context
    # Test Case to validate SF ARRAY_SLICE conversion to SLICE in Databricks
    validate_source_transpile(
        "SELECT SLICE(ARRAY(0, 1, 2, 3, 4, 5, 6), 1, 2)",
        source={
            "snowflake": "SELECT array_slice(array_construct(0,1,2,3,4,5,6), 0, 2);",
        },
    )
    # Test Case to validate SF ARRAY_SLICE conversion to SLICE in Databricks with negative `from`
    validate_source_transpile(
        "SELECT SLICE(ARRAY(90, 91, 92, 93, 94, 95, 96), -5, 3)",
        source={
            "snowflake": "SELECT array_slice(array_construct(90,91,92,93,94,95,96), -5, 3);",
        },
    )
    with pytest.raises(UnsupportedError):
        # Test Case to validate SF ARRAY_SLICE conversion to SLICE in Databricks with negative `to`
        # In Databricks: function `slice` length must be greater than or equal to 0
        validate_source_transpile(
            "SELECT SLICE(ARRAY(90, 91, 92, 93, 94, 95, 96), -4, -1)",
            source={
                "snowflake": "SELECT array_slice(array_construct(90,91,92,93,94,95,96), -4, -1);",
            },
        )


def test_create_ddl(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        """
            create table employee (employee_id decimal(38, 0),
                first_name string not null,
                last_name string not null,
                birth_date date,
                hire_date date,
                salary decimal(10, 2),
                department_id decimal(38, 0))
        """,
        source={
            "snowflake": """
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


def test_delete_from_keyword(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "DELETE FROM employee WHERE employee_id = 1;",
        source={
            "snowflake": "DELETE FROM employee WHERE employee_id = 1",
        },
    )

    validate_source_transpile(
        "MERGE INTO  TABLE1 using table2 on table1.id = table2.id when matched then delete;",
        source={
            "snowflake": "DELETE FROM Table1 USING table2 WHERE table1.id = table2.id;",
        },
    )


def test_nested_query_with_json(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        """SELECT a.col1, a.col2, b.col3, b.col4 FROM (SELECT col1, col2 FROM table1) AS a, 
        (SELECT CAST(value.price AS DOUBLE) AS col3, col4 
        FROM (SELECT * FROM table2) AS k) AS b WHERE a.col1 = b.col4""",
        source={
            "snowflake": """SELECT A.COL1, A.COL2, B.COL3, B.COL4 FROM 
                            (SELECT COL1, COL2 FROM TABLE1) A, 
                            (SELECT VALUE:PRICE::FLOAT AS COL3, COL4 FROM 
                            (SELECT * FROM TABLE2 ) AS K
                            ) B 
                            WHERE A.COL1 = B.COL4;""",
        },
    )


def test_update_from_dml(dialect_context):
    validate_source_transpile, _ = dialect_context
    validate_source_transpile(
        "MERGE INTO t1 USING t2 ON t1.key = t2.t1_key and t1.column1 < 10 WHEN MATCHED THEN UPDATE "
        "SET column1 = t1.column1 + t2.column1, t1.column3 = 'success'",
        source={
            "snowflake": """UPDATE t1
                            SET column1 = t1.column1 + t2.column1, t1.column3 = 'success'
                            FROM t2
                            WHERE t1.key = t2.t1_key and t1.column1 < 10;""",
        },
    )

    validate_source_transpile(
        "MERGE INTO target USING (SELECT k, MIN(v) AS v FROM src GROUP BY k) AS b ON target.k = b.k WHEN MATCHED THEN "
        "UPDATE SET v = b.v  ",
        source={
            "snowflake": """UPDATE target
                            SET v = b.v
                            FROM (SELECT k, MIN(v) v FROM src GROUP BY k) b
                            WHERE target.k = b.k;""",
        },
    )
    validate_source_transpile(
        "UPDATE orders AS t1 SET order_status = 'returned' WHERE EXISTS(SELECT oid FROM returned_orders "
        "WHERE t1.oid = oid)",
        source={
            "snowflake": """UPDATE orders t1
                            SET order_status = 'returned'
                            WHERE EXISTS (SELECT oid FROM returned_orders WHERE t1.oid = oid);""",
        },
    )
