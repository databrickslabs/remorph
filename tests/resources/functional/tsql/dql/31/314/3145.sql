-- tsql sql:
WITH ProductResultsCTE AS ( SELECT ProductID, ProductName FROM ( VALUES (1, 'Product1'), (2, 'Product2') ) AS ProductResults (ProductID, ProductName) ) SELECT ProductID, ProductName FROM ProductResultsCTE;
