-- see https://docs.snowflake.com/en/sql-reference/functions/uniform

SELECT uniform(1, 10, 1234) FROM table(generator(rowCount => 5));
