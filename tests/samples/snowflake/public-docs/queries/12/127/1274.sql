-- see https://docs.snowflake.com/en/sql-reference/functions/object_delete

SELECT OBJECT_DELETE(OBJECT_CONSTRUCT('a', 1, 'b', 2, 'c', 3), 'a', 'b');
