--Query type: DQL
WITH CustomerCTE AS (
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES
            (1, 'Customer1', 'Address1'),
            (2, 'Customer2', 'Address2'),
            (3, 'Customer3', 'Address3')
    ) AS Customer (c_custkey, c_name, c_address)
)
SELECT c_custkey, c_name
FROM CustomerCTE
WHERE c_custkey <= 500
    AND c_name LIKE '%Smi%'
    AND c_address LIKE '%A%';