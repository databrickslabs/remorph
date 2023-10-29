-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/case-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks

SELECT ProductAlternateKey,
    Category = CASE ProductLine
        WHEN 'R' THEN 'Road'
        WHEN 'M' THEN 'Mountain'
        WHEN 'T' THEN 'Touring'
        WHEN 'S' THEN 'Other sale items'
        ELSE 'Not for sale'
        END,
    EnglishProductName
FROM dbo.DimProduct
ORDER BY ProductKey;
GO