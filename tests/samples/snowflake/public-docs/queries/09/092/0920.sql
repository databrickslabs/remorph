-- see https://docs.snowflake.com/en/sql-reference/constructs/sample

SELECT * FROM testtable SAMPLE BLOCK (0.012) REPEATABLE (99992);