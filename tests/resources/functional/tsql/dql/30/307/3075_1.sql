--Query type: DQL
WITH CustomerCTE AS (
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES (1, 'Customer1', 'Address1'),
               (2, 'Customer2', 'Address2')
    ) AS Customer (c_custkey, c_name, c_address)
)
SELECT c_custkey, c_name, c_address, dbo.GetCustomerType(c_custkey) AS CustomerType
FROM CustomerCTE;