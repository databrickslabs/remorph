-- tsql sql:
CREATE TABLE Product
(
    ProductID INT,
    ProductName VARCHAR(50),
    ProductDescription VARCHAR(200)
);

INSERT INTO Product (ProductID, ProductName, ProductDescription)
VALUES
    (1, 'Product A', 'This is product A'),
    (2, 'Product B', 'This is product B'),
    (3, 'Product C', NULL);

WITH cte AS
(
    SELECT ProductID, ProductName, ProductDescription
    FROM (
        VALUES (1, 'Product A', 'This is product A'),
               (2, 'Product B', 'This is product B'),
               (3, 'Product C', NULL)
    ) AS p (ProductID, ProductName, ProductDescription)
)
UPDATE p
SET p.ProductDescription = 'Replacing NULL value'
FROM Product p
INNER JOIN cte c ON p.ProductID = c.ProductID
WHERE c.ProductName = 'Product C';

SELECT * FROM Product;
-- REMORPH CLEANUP: DROP TABLE Product;
