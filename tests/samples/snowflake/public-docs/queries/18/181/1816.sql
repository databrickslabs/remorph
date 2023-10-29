-- see https://docs.snowflake.com/en/sql-reference/functions/get_path

SELECT v:attr[0].name FROM vartab;