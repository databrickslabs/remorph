-- see https://docs.snowflake.com/en/sql-reference/functions/randstr

SELECT randstr(abs(random()) % 10, random()) FROM table(generator(rowCount => 5));
