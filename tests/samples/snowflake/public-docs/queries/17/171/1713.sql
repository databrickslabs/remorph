-- see https://docs.snowflake.com/en/sql-reference/functions/random

SELECT random() FROM table(generator(rowCount => 3));
