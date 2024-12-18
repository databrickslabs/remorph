-- tsql sql:
SELECT LEFT(v.value, 2) AS result FROM (VALUES ('abcdefghij')) AS v(value);
