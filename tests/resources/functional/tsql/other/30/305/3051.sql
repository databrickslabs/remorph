-- tsql sql:
CREATE TABLE CustomerStats
(
    CustomerID INT,
    CustomerName VARCHAR(50),
    CustomerStats1 INT
);

INSERT INTO CustomerStats
(
    CustomerID,
    CustomerName,
    CustomerStats1
)
SELECT *
FROM (
    VALUES
    (
        1,
        'John Doe',
        10
    ),
    (
        2,
        'Jane Doe',
        20
    ),
    (
        3,
        'Bob Smith',
        30
    )
) AS Customer
(
    CustomerID,
    CustomerName,
    CustomerStats1
);

UPDATE STATISTICS CustomerStats (CustomerStats1);

SELECT *
FROM CustomerStats;
-- REMORPH CLEANUP: DROP TABLE CustomerStats;
