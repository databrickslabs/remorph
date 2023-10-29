-- see https://docs.snowflake.com/en/sql-reference/constructs/from

SELECT v.profit 
    FROM (SELECT retail_price - wholesale_cost AS profit FROM ftable1) AS v;