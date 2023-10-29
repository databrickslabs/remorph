-- see https://docs.snowflake.com/en/sql-reference/functions/flatten

SELECT * FROM TABLE(FLATTEN(input => parse_json('[1, ,77]'))) f;
