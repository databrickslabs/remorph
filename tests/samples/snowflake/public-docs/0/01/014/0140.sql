SELECT product_ID, SUM(retail_price * quantity) AS gross_revenue
  FROM sales
  GROUP BY product_ID;