-- see https://docs.snowflake.com/en/sql-reference/functions/random

SELECT random(4711) FROM table(generator(rowCount => 3));