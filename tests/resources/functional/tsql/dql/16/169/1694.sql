--Query type: DQL
DECLARE @customer geometry = 'COMPOUNDCURVE(CIRCULARSTRING(0 0, 8 8, 16 0, 20 -4, 24 0),(24 0, 20 4, 16 0))';
WITH customer AS (
    SELECT @customer.Reduce(15).ToString() AS customer
)
SELECT customer
FROM customer
UNION ALL
SELECT @customer.Reduce(16).ToString() AS customer
