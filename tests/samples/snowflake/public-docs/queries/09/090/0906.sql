-- see https://docs.snowflake.com/en/sql-reference/constructs/at-before

SELECT * FROM my_table BEFORE(STATEMENT => '8e5d0ca9-005e-44e6-b858-a8f5b37c5726');