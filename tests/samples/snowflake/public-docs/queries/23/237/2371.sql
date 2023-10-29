-- see https://docs.snowflake.com/en/sql-reference/sql-format-models

select to_char(1234, '9d999EE'), 'will look like', '1.234E3';