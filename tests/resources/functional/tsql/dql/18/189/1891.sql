--Query type: DQL
DECLARE @supplier_city VARCHAR(10) = 'NEW YORK';
DECLARE @supplier_name VARCHAR(20) = @supplier_city;
SELECT *
FROM (
    VALUES (@supplier_name, @supplier_city)
) AS temp_result (SupplierName, SupplierCity);
