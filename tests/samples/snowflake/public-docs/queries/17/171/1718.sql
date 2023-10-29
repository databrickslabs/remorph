-- see https://docs.snowflake.com/en/sql-reference/functions/randstr

SELECT randstr(5, random()) FROM table(generator(rowCount => 5));
