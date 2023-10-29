-- see https://docs.snowflake.com/en/sql-reference/functions/split_part

SELECT SPLIT_PART('aaa--bbb-BBB--ccc', '--', 2);