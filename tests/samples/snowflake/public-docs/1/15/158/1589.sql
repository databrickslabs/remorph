SELECT 
    sale_date, 
    price,
    WIDTH_BUCKET(price, 200000, 600000, 4) AS "SALES GROUP"
  FROM home_sales
  ORDER BY sale_date;