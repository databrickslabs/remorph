-- see https://docs.snowflake.com/en/sql-reference/constructs/group-by

select sum(salary), ANY_VALUE(employment_state)
    from employees
    group by employment_state;