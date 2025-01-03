-- snowflake sql:
WITH orders AS (
  SELECT
    101 AS order_id,
    ARRAY_CONSTRUCT(
      OBJECT_CONSTRUCT('product_id', 1, 'name', 'ProductA'),
      OBJECT_CONSTRUCT('product_id', 2, 'name', 'ProductB')
    ) AS order_details
  UNION ALL
  SELECT
    102 AS order_id,
    ARRAY_CONSTRUCT(
      OBJECT_CONSTRUCT('product_id', 3, 'name', 'ProductC')
    ) AS order_details
)
SELECT
  order_id,
  value AS product
FROM
  orders,
  LATERAL FLATTEN(input => order_details) as value;

-- databricks sql:
WITH orders AS (
  SELECT
    101 AS order_id,
    ARRAY(
      STRUCT(1 AS product_id, 'ProductA' AS name),
      STRUCT(2 AS product_id, 'ProductB' AS name)
    ) AS order_details
  UNION ALL
  SELECT
    102 AS order_id,
    ARRAY(STRUCT(3 AS product_id, 'ProductC' AS name)) AS order_details
)
SELECT
  order_id,
  value AS product
FROM
  orders LATERAL VIEW EXPLODE(order_details) AS value
