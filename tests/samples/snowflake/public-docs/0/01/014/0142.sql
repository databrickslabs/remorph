SELECT p.product_ID, SUM((s.retail_price - p.wholesale_price) * s.quantity) AS profit
  FROM products AS p, sales AS s
  WHERE s.product_ID = p.product_ID
  GROUP BY p.product_ID;