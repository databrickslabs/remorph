-- see https://docs.snowflake.com/en/sql-reference/functions/parse_json

UPDATE jdemo2 SET
    variant1 = PARSE_JSON(varchar1),
    variant2 = TO_VARIANT(varchar1);