-- see https://docs.snowflake.com/en/sql-reference/functions/is

select count(*) from vartab where is_char(v);
