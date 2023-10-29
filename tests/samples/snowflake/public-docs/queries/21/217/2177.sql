-- see https://docs.snowflake.com/en/sql-reference/functions/skew

select SKEW(K), SKEW(V), SKEW(V2) 
    from aggr;