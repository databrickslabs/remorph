-- see https://docs.snowflake.com/en/sql-reference/functions/zipf

SELECT zipf(1, 10, 1234) FROM table(generator(rowCount => 10));
