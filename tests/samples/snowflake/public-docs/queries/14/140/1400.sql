-- see https://docs.snowflake.com/en/sql-reference/constructs/group-by

SELECT SUM(amount)
  FROM mytable
  GROUP BY ALL;