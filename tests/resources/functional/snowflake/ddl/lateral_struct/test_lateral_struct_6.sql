-- snowflake sql:
SELECT ARRAY_EXCEPT([{'a': 1, 'b': 2}, 1], [{'a': 1, 'b': 2}, 3]);

-- revised snowflake sql
SELECT ARRAY_EXCEPT([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}], [{'a': 1, 'b': 2}, {'a': 1, 'b': 2}]);

-- databricks sql:
SELECT ARRAY_EXCEPT(ARRAY(STRUCT(1 AS a, 2 AS b), 1), ARRAY(STRUCT(1 AS a, 2 AS b), 3));

-- revised databricks sql
SELECT ARRAY_EXCEPT(
  ARRAY(STRUCT(1 AS a, 2 AS b), STRUCT(3 AS a, 4 AS b)),
  ARRAY(STRUCT(1 AS a, 2 AS b), STRUCT(1 AS a, 2 AS b))
);
