-- see https://docs.snowflake.com/en/sql-reference/functions/normal

SELECT normal(0, 1, 1234) FROM table(generator(rowCount => 5));
