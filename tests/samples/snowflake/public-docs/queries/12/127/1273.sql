-- see https://docs.snowflake.com/en/sql-reference/functions/object_construct

SELECT OBJECT_CONSTRUCT(*) FROM VALUES(1,'x'), (2,'y');