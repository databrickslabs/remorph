-- see https://docs.snowflake.com/en/sql-reference/constructs/sample

SELECT * FROM testtable TABLESAMPLE BERNOULLI (20.3);