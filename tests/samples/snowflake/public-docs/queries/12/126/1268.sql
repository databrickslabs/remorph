-- see https://docs.snowflake.com/en/sql-reference/functions/object_construct

SELECT OBJECT_CONSTRUCT('Key_One', PARSE_JSON('NULL'), 'Key_Two', NULL, 'Key_Three', 'null') as obj;