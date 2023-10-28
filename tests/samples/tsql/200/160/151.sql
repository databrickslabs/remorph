-- Uses AdventureWorks
  
SELECT CustomerKey,
    LastName
FROM (
    SELECT *
    FROM DimCustomer
    WHERE BirthDate > '01/01/1970'
    ) AS DimCustomerDerivedTable
WHERE LastName = 'Smith'
ORDER BY LastName;