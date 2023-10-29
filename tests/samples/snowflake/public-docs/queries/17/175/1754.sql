-- see https://docs.snowflake.com/en/sql-reference/constructs/group-by

SELECT state, city, SUM(retail_price * quantity) AS gross_revenue
  FROM sales
  GROUP BY state, city;