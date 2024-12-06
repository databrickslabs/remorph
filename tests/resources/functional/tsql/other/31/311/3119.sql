-- tsql sql:
CREATE TABLE Products (
    product_id VARCHAR(10),
    list_price DECIMAL(10, 2)
);

INSERT INTO Products (
    product_id,
    list_price
)
VALUES
    ('BK-1', 100.00),
    ('BK-2', 200.00),
    ('BK-3', 300.00);

BEGIN TRANSACTION UpdateListPrices WITH MARK 'UPDATE Product list prices';

WITH updated_products AS (
    SELECT product_id, list_price * 1.10 AS new_list_price
    FROM Products
    WHERE product_id LIKE 'BK-%'
)
UPDATE p
SET list_price = up.new_list_price
FROM Products p
INNER JOIN updated_products up ON p.product_id = up.product_id;

COMMIT TRANSACTION UpdateListPrices;

SELECT * FROM Products;
