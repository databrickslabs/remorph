--Query type: DML
CREATE TABLE #products (product_ID INT, wholesale_price DECIMAL(10, 2));
INSERT INTO #products (product_ID, wholesale_price)
SELECT *
FROM (VALUES (1, 1.00), (2, 2.00)) AS products (product_ID, wholesale_price);