-- see https://docs.snowflake.com/en/sql-reference/sql-format-models

select to_varchar(f, '999,999.999'), to_varchar(f, 'S999,999.999') from sample_numbers;