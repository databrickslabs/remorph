-- tsql sql:
CREATE TABLE #orders
(
    orderkey INT,
    totalprice DECIMAL(10, 2)
);

INSERT INTO #orders (orderkey, totalprice)
VALUES
    (1, 100.0),
    (2, 200.0),
    (3, 300.0);

CREATE INDEX idx_orders
ON #orders (totalprice);

SELECT *
FROM #orders;

-- REMORPH CLEANUP: DROP TABLE #orders;
