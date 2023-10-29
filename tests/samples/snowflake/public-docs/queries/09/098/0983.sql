-- see https://docs.snowflake.com/en/sql-reference/functions/array_except

SELECT ARRAY_EXCEPT([{'a': 1, 'b': 2}, 1], [{'a': 1, 'b': 2}, 3]);
