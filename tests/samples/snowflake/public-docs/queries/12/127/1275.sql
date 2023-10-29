-- see https://docs.snowflake.com/en/sql-reference/functions/object_insert

SELECT OBJECT_INSERT(OBJECT_CONSTRUCT('a',1,'b',2),'c',3);
