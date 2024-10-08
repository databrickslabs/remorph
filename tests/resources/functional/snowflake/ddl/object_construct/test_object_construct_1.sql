
-- snowflake sql:
SELECT OBJECT_CONSTRUCT('a',1,'b','BBBB', 'i',null);

-- databricks sql:
SELECT STRUCT(1 AS a, 'BBBB' AS b, NULL AS i);
