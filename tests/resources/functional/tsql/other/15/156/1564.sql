-- tsql sql:
DECLARE @total DECIMAL(10, 2) = (SELECT SUM(total) FROM (VALUES (100.00), (200.00), (300.00)) AS totals(total))
