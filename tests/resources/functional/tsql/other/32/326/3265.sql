-- tsql sql:
WITH deliveries AS (
  SELECT
    5000 + ROW_NUMBER() OVER (ORDER BY n.n) AS order_id,
    n.n AS cust_id,
    GETDATE() AS order_date,
    DATEADD(dd, 10, GETDATE()) AS delivery_date,
    SESSION_USER AS received_shipment
  FROM
    (VALUES (1), (2), (3), (4), (5)) n(n)
)
SELECT
  order_id,
  cust_id,
  order_date,
  delivery_date,
  received_shipment
INTO #deliveries3
FROM
  deliveries;
-- REMORPH CLEANUP: DROP TABLE #deliveries3;
