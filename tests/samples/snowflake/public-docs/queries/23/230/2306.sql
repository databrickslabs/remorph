-- see https://docs.snowflake.com/en/sql-reference/data-types-datetime

select name, hire_date from employees where hire_date > current_date - INTERVAL '2 y, 3 month';