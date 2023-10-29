-- see https://docs.snowflake.com/en/sql-reference/functions/to_json

SELECT TO_JSON(NULL), TO_JSON('null'::VARIANT),
       PARSE_JSON(NULL), PARSE_JSON('null');