-- source:
SELECT
  {'a': 1,'b' : 2},
  [{'c': 11,'d' : 22}, 3];
-- databricks_sql:
SELECT
  STRUCT(1 AS a, 2 AS b),
  ARRAY(STRUCT(11 AS C, 22 AS d), 3)
