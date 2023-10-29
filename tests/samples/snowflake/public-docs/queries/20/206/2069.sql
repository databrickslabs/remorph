-- see https://docs.snowflake.com/en/sql-reference/functions/kurtosis

select *
    from aggr
    order by k, v;