-- see https://docs.snowflake.com/en/sql-reference/functions/as

select avg(as_real(v)) from vartab;