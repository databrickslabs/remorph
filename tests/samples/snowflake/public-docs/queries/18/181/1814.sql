-- see https://docs.snowflake.com/en/sql-reference/constructs/values

SELECT v1.$2, v2.$2
  FROM (VALUES (1, 'one'), (2, 'two')) AS v1
        INNER JOIN (VALUES (1, 'One'), (3, 'three')) AS v2
  WHERE v2.$1 = v1.$1;