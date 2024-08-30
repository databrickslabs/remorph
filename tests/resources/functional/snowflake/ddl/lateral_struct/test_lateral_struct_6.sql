-- snowflake sql:
SELECT ARRAY_EXCEPT([{'a': 1, 'b': 2}, 1], [{'a': 1, 'b': 2}, 3]);

-- databricks sql:
SELECT ARRAY_EXCEPT(ARRAY(STRUCT(1 AS a, 2 AS b), 1), ARRAY(STRUCT(1 AS a, 2 AS b), 3));
