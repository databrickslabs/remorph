-- see https://docs.snowflake.com/en/sql-reference/functions/check_json

SELECT ID, CHECK_JSON(variant1), variant1 FROM sample_json_table ORDER BY ID;