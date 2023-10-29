-- see https://docs.snowflake.com/en/sql-reference/functions/split_part

SELECT SPLIT_PART('|a|b|c|', '|', 1), SPLIT_PART('|a|b|c|', '|', 2);