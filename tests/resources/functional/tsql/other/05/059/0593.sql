--Query type: DDL
SELECT *
INTO #Sales
FROM (
    VALUES (
        1, 'Sale1', 100.0
        , (2, 'Sale2', 200.0)
        , (3, 'Sale3', 300.0)
    )
) AS Sales (
    SaleID
    , SaleName
    , SaleAmount
);

CREATE INDEX idx_SaleID
ON #Sales (
    SaleID
);

ALTER INDEX idx_SaleID
ON #Sales
DISABLE;