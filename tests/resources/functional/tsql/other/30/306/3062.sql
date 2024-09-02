--Query type: DML
CREATE TABLE #Products
(
    ProductID INT,
    ProductName VARCHAR(50)
);

INSERT INTO #Products
(
    ProductID,
    ProductName
)
VALUES
(
    50,
    'Screwdriver'
),
(
    60,
    'Hammer'
);

UPDATE #Products
SET ProductName = 'Flat Head Screwdriver'
WHERE ProductID = 50;

SELECT *
FROM #Products;

-- REMORPH CLEANUP: DROP TABLE #Products;