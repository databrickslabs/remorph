--Query type: DQL
WITH CustomerCTE AS (
    SELECT 1 AS CustomerID, 'John' AS FirstName, 'Doe' AS LastName, '123-456-7890' AS PhoneNumber
    UNION ALL
    SELECT 2, 'Jane', 'Doe', '987-654-3210'
),
PhoneCTE AS (
    SELECT 1 AS CustomerID, '123-456-7890' AS PhoneNumber
    UNION ALL
    SELECT 2, '987-654-3210'
)
SELECT c.CustomerID, c.FirstName, c.LastName, c.PhoneNumber AS Phone
FROM CustomerCTE c
JOIN PhoneCTE p ON c.CustomerID = p.CustomerID
WHERE c.LastName LIKE 'D%'
ORDER BY c.LastName, c.FirstName
FOR XML AUTO, TYPE, XMLSCHEMA, ELEMENTS XSINIL;