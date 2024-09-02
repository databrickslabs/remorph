--Query type: DML
CREATE TABLE OrderDetails
(
    OrderDetailID INT,
    OrderID INT,
    ProductID INT,
    DueDate DATE
);

INSERT INTO OrderDetails
(
    OrderDetailID,
    OrderID,
    ProductID,
    DueDate
)
VALUES
(
    1,
    1,
    1,
    '2022-01-01'
),
(
    2,
    1,
    2,
    '2022-01-15'
),
(
    3,
    2,
    3,
    '2022-02-01'
),
(
    4,
    2,
    4,
    '2022-02-15'
),
(
    5,
    3,
    5,
    '2022-03-01'
),
(
    6,
    3,
    6,
    '2022-03-15'
),
(
    7,
    4,
    7,
    '2022-04-01'
),
(
    8,
    4,
    8,
    '2022-04-15'
),
(
    9,
    5,
    9,
    '2022-05-01'
),
(
    10,
    5,
    10,
    '2022-05-15'
);

WITH TopOrderDetails AS
(
    SELECT TOP 10 OrderDetailID
    FROM OrderDetails
    ORDER BY DueDate ASC
)
DELETE FROM OrderDetails
WHERE OrderDetailID IN
(
    SELECT OrderDetailID
    FROM TopOrderDetails
);

SELECT *
FROM OrderDetails;
-- REMORPH CLEANUP: DROP TABLE OrderDetails;