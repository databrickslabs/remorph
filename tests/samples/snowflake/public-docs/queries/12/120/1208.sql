-- see https://docs.snowflake.com/en/sql-reference/functions/check_json

SELECT ID, CHECK_JSON(varchar1), varchar1 FROM sample_json_table ORDER BY ID;