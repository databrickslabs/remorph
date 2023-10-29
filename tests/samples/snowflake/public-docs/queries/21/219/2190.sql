-- see https://docs.snowflake.com/en/sql-reference/data-types-semistructured

select array_slice(array_column, 6, 8) from table_1;