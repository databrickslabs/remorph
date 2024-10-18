--Query type: DML
CREATE TABLE #ShoppingCartItem
(
    ShoppingCartID INT,
    ItemName VARCHAR(50)
);

INSERT INTO #ShoppingCartItem
(
    ShoppingCartID,
    ItemName
)
VALUES
(
    20621,
    'Item1'
),
(
    20621,
    'Item2'
),
(
    20622,
    'Item3'
);

DELETE FROM #ShoppingCartItem
OUTPUT DELETED.*
WHERE ShoppingCartID = 20621;

SELECT COUNT(*) AS [Rows in Table]
FROM #ShoppingCartItem
WHERE ShoppingCartID = 20621;

-- REMORPH CLEANUP: DROP TABLE #ShoppingCartItem;