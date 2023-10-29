-- see https://docs.snowflake.com/en/sql-reference/constructs/sample

SELECT * FROM testtable SAMPLE SYSTEM (3) SEED (82);