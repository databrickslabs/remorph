--Query type: DML
CREATE TABLE ##TempResult
(
    OrderItemID INT,
    OrderID INT,
    ProductID INT,
    Quantity INT
);

INSERT INTO ##TempResult
(
    OrderItemID,
    OrderID,
    ProductID,
    Quantity
)
VALUES
(
    1,
    1,
    1,
    10
);

DBCC INDEXDEFRAG (0, '##TempResult');

SELECT *
FROM ##TempResult;

-- REMORPH CLEANUP: DROP TABLE ##TempResult;
