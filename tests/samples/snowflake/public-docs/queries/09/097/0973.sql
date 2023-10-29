-- see https://docs.snowflake.com/en/sql-reference/functions/array_distinct

SELECT ARRAY_DISTINCT( [ {'a': 1, 'b': 2}, {'a': 1, 'b': 2}, {'a': 1, 'b': 3} ] );
