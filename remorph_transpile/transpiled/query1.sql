SELECT
  i_manufact,
  SUM(ss_ext_sales_price) AS ext_price
FROM date_dim, store_sales
WHERE
  d_date_sk = ss_sold_date_sk AND SUBSTR(ca_zip, 1, 5) <> SUBSTR(s_zip, 1, 5)
GROUP BY
  i_manufact
ORDER BY
  i_manufact NULLS LAST
LIMIT 100
;
