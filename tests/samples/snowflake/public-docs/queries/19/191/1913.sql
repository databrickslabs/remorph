-- see https://docs.snowflake.com/en/sql-reference/data-types-semistructured

UPDATE my_table SET my_array = [ 1, 2 ];

UPDATE my_table SET my_array = ARRAY_CONSTRUCT(1, 2);