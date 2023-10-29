-- see https://docs.snowflake.com/en/sql-reference/functions/uniform

SELECT uniform(1, 10, random()) FROM table(generator(rowCount => 5));
