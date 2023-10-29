-- see https://docs.snowflake.com/en/sql-reference/data-types-datetime

select name from employees where end_date > start_date + 365;