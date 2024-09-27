
-- snowflake sql:
SELECT {'a': 1, 'b': 2}, [{'c': 11, 'd': 22}, 3];

-- databricks sql:
SELECT STRUCT(1 AS a, 2 AS b), ARRAY(STRUCT(11 AS c, 22 AS d), 3);


