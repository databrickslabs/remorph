-- see https://docs.snowflake.com/en/sql-reference/operators-logical

SELECT x AS "OR", x OR False AS "FALSE", x OR True AS "TRUE", x OR NULL AS "NULL"
  FROM logical2;