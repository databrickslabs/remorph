-- see https://docs.snowflake.com/en/sql-reference/constructs/values

SELECT c1, c2
  FROM (VALUES (1, 'one'), (2, 'two')) AS v1 (c1, c2);