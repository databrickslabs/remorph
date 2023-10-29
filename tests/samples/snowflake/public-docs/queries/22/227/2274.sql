-- see https://docs.snowflake.com/en/sql-reference/functions/mode

select k, mode(v) 
    from aggr 
    group by k
    order by k;