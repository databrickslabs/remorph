select sum(salary), ANY_VALUE(employment_state) as state
    from employees
    group by state;