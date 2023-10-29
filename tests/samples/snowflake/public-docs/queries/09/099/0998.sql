-- see https://docs.snowflake.com/en/sql-reference/functions/array_max

SELECT ARRAY_MAX([NULL, PARSE_JSON('null'), NULL]);