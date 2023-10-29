-- see https://docs.snowflake.com/en/sql-reference/functions/kurtosis

select KURTOSIS(K), KURTOSIS(V), KURTOSIS(V2) 
    from aggr;