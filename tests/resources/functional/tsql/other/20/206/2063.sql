--Query type: DML
EXEC sp_create_plan_guide @name = N'Guide3', @stmt = N'WITH CustomerCTE AS (
    SELECT CustomerID, ContactID, SalesPersonID, CompanyName
    FROM (
        VALUES (1, 1, 2, ''ABC Inc.''),
               (2, 2, 1, ''XYZ Corp.''),
               (3, 3, 2, ''DEF Ltd.'')
    ) AS Customer(CustomerID, ContactID, SalesPersonID, CompanyName)
),
SalesPersonCTE AS (
    SELECT SalesPersonID, LastName, FirstName
    FROM (
        VALUES (1, ''Doe'', ''John''),
               (2, ''Smith'', ''Jane''),
               (3, ''Johnson'', ''Bob'')
    ) AS SalesPerson(SalesPersonID, LastName, FirstName)
)
SELECT s.LastName, s.FirstName, c.CompanyName
FROM CustomerCTE c
JOIN SalesPersonCTE s ON c.SalesPersonID = s.SalesPersonID
WHERE c.SalesPersonID = 2
OPTION (TABLE HINT(c, INDEX (IX_Customer_SalesPersonID)));', @type = N'SQL', @module_or_batch = NULL, @params = NULL, @hints = N'OPTION (TABLE HINT(c, INDEX (IX_Customer_SalesPersonID)))';