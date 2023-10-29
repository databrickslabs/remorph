-- see https://docs.snowflake.com/en/sql-reference/functions/get_path

SELECT GET_PATH('v:"attr"[0]:"name"') FROM vartab;