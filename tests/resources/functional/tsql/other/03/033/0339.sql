-- tsql sql:
CREATE TABLE Products
(
    ProductKey INT,
    ProductSubcategoryKey INT
);

INSERT INTO Products
(
    ProductKey,
    ProductSubcategoryKey
)
VALUES
(
    313,
    1
);

WITH p AS
(
    SELECT ProductKey, ProductSubcategoryKey
    FROM Products
    WHERE ProductKey = 313
)
UPDATE p
SET ProductSubcategoryKey = 2
OPTION (LABEL = N'label3');

SELECT * FROM Products;
