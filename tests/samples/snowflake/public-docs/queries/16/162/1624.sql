-- see https://docs.snowflake.com/en/sql-reference/functions/lag

SELECT emp_id, year, revenue, 
       revenue - LAG(revenue, 1, 0) OVER (PARTITION BY emp_id ORDER BY year) AS diff_to_prev 
    FROM sales 
    ORDER BY emp_id, year;