-- see https://docs.snowflake.com/en/sql-reference/collation

SELECT DISTINCT COLLATION(c1), COLLATION(c2) FROM collation_demo2;