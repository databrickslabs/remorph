-- see https://docs.snowflake.com/en/sql-reference/sql/update

UPDATE target SET v = b.v
  FROM (SELECT k, MIN(v) v FROM src GROUP BY k) b
  WHERE target.k = b.k;