-- snowflake sql:
INSERT INTO foo (c1, c2, c3)
    SELECT x, y, z FROM bar WHERE x > z AND y = 'qux';

-- databricks sql:
INSERT INTO foo (
  c1,
  c2,
  c3
)
SELECT
  x,
  y,
  z
FROM bar
WHERE
  x > z AND y = 'qux';
