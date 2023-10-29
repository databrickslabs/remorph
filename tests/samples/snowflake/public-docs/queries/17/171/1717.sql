-- see https://docs.snowflake.com/en/sql-reference/functions/randstr

SELECT randstr(5, 1234) FROM table(generator(rowCount => 5));
