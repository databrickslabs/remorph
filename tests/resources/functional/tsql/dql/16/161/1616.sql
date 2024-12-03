--Query type: DQL
DECLARE @customer geography = 'POLYGON ((-0.5 0, 0 1, 0.5 0.5, -0.5 0))';
DECLARE @supplier geography = 'CURVEPOLYGON(COMPOUNDCURVE(CIRCULARSTRING(0 0, 0.7 0.7, 0 1), (0 1, 0 0)))';
WITH customer_region AS (
  SELECT @customer AS customer
),
supplier_region AS (
  SELECT @supplier AS supplier
)
SELECT cr.customer.STUnion(sr.supplier).ToString()
FROM customer_region cr
CROSS JOIN supplier_region sr;
