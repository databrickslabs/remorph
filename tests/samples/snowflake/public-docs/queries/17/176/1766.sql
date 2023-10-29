-- see https://docs.snowflake.com/en/sql-reference/constructs/join

SELECT t1.*, t2.*, t3.*
  FROM t1
     LEFT OUTER JOIN t2 ON (t1.col1 = t2.col1)
     RIGHT OUTER JOIN t3 ON (t3.col1 = t2.col1)
  ORDER BY t1.col1;