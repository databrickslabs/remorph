-- see https://docs.snowflake.com/en/sql-reference/constructs/at-before

SELECT * FROM my_table AT(TIMESTAMP => TO_TIMESTAMP(1432669154242, 3));