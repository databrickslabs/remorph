-- see https://docs.snowflake.com/en/sql-reference/functions/object_insert

SELECT
  OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_CONSTRUCT(), 'Key_One', PARSE_JSON('NULL')), 'Key_Two', NULL), 'Key_Three', 'null')
  AS obj;
