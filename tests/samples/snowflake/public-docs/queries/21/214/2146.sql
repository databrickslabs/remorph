-- see https://docs.snowflake.com/en/sql-reference/functions/skew

select * 
    from aggr
    order by k, v;