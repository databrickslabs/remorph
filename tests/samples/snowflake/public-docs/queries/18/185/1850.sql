-- see https://docs.snowflake.com/en/sql-reference/functions/zipf

SELECT zipf(1, 10, random()) FROM table(generator(rowCount => 10));
