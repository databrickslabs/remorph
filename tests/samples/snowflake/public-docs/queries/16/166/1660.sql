-- see https://docs.snowflake.com/en/sql-reference/functions/var_samp

SELECT k, var_samp(v), var_samp(v2) 
    FROM aggr 
    GROUP BY k
    ORDER BY k;