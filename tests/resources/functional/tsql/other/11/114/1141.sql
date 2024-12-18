-- tsql sql:
CREATE TABLE ProductProperties
(
    ProductID INT,
    ProductName VARCHAR(50),
    ProductDescription VARCHAR(200)
);

INSERT INTO ProductProperties
(
    ProductID,
    ProductName,
    ProductDescription
)
VALUES
(
    1,
    'Product 1',
    'This is product 1'
),
(
    2,
    'Product 2',
    'This is product 2'
),
(
    3,
    'Product 3',
    'This is product 3'
);

SELECT *
FROM ProductProperties;

-- REMORPH CLEANUP: DROP TABLE ProductProperties;
