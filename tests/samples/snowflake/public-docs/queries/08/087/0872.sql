-- see https://docs.snowflake.com/en/sql-reference/functions/flatten

SELECT * FROM TABLE(FLATTEN(input => parse_json('[]'))) f;


SELECT * FROM TABLE(FLATTEN(input => parse_json('[]'), outer => true)) f;
