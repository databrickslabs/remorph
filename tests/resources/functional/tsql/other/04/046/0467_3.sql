--Query type: DCL
DECLARE @customerkey INT;
SELECT *
FROM (
    VALUES (@customerkey, 'Customer1'),
           (@customerkey, 'Customer2')
) AS Customer (customerkey, name);
