-- see https://docs.snowflake.com/en/sql-reference/functions/seq1

SELECT seq8() FROM table(generator(rowCount => 5));
