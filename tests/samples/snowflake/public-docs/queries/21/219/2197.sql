-- see https://docs.snowflake.com/en/sql-reference/data-types-semistructured

select array_slice(my_array_column, 5, 10) from my_table;