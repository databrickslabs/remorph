-- tsql sql:
CREATE TABLE #orders
(
    order_id INT,
    order_name VARCHAR(50)
);

CREATE TABLE #lineitems
(
    order_id INT,
    line_number INT,
    quantity DECIMAL(10, 2)
);

INSERT INTO #orders (order_id, order_name)
VALUES
    (1, 'o1'),
    (2, 'o2');

INSERT INTO #lineitems (order_id, line_number, quantity)
VALUES
    (1, 1, 10.0),
    (2, 1, 20.0);

BEGIN TRANSACTION;

WITH orders AS
(
    SELECT *
    FROM #orders
),
lineitems AS
(
    SELECT *
    FROM #lineitems
)
DELETE o
FROM orders o
JOIN lineitems l ON o.order_id = l.order_id
WHERE l.quantity > 15;

TRUNCATE TABLE #lineitems;

COMMIT TRANSACTION;

SELECT *
FROM #orders;

-- REMORPH CLEANUP: DROP TABLE #orders;
-- REMORPH CLEANUP: DROP TABLE #lineitems;
