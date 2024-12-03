--Query type: DQL
DECLARE @supplier_name VARCHAR(64);
SELECT @supplier_name = 'Supplier#000000001' + ' is a regular supplier.';
WITH supplier AS (
    SELECT 'Supplier#000000001' AS name, 'regular' AS type
)
SELECT CHARINDEX('regular', @supplier_name) AS position
FROM supplier;
