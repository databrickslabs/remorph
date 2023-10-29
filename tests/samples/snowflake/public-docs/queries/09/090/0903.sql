-- see https://docs.snowflake.com/en/sql-reference/constructs/at-before

SELECT * FROM my_table AT(OFFSET => -60*5) AS T WHERE T.flag = 'valid';