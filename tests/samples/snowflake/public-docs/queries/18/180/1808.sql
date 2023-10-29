-- see https://docs.snowflake.com/en/sql-reference/functions/to_json

SELECT v, v:food, TO_JSON(v) FROM jdemo1;