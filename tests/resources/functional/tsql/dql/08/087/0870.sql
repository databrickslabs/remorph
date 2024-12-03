--Query type: DQL
DECLARE @binding VARCHAR(50) = 'Customer#1';
WITH CustomerCTE AS (
    SELECT *
    FROM (
        VALUES ('Customer#1', 'Smith'),
               ('Customer#2', 'Johnson')
    ) AS Customer (CustKey, CustName)
)
SELECT *
FROM CustomerCTE
WHERE CustKey = @binding;
