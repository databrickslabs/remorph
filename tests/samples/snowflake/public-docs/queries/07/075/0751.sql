-- see https://docs.snowflake.com/en/sql-reference/functions-analytic

SELECT
    salesperson_name,
    sales_in_dollars,
    RANK() OVER (ORDER BY sales_in_dollars DESC) AS sales_rank
  FROM sales_table
  ORDER BY 3;