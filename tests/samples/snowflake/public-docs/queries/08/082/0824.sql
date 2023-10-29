-- see https://docs.snowflake.com/en/sql-reference/constructs/join

SELECT *
  FROM d1 NATURAL FULL OUTER JOIN d2
  ORDER BY ID;