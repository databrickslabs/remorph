-- see https://docs.snowflake.com/en/sql-reference/functions/split_part

SELECT SPLIT_PART('127.0.0.1', '.', 1), SPLIT_PART('127.0.0.1', '.', -1);