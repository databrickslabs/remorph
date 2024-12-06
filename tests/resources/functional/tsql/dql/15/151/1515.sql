-- tsql sql:
DECLARE @customer_array VARCHAR(MAX);
SET @customer_array = '[{"name":"Customer#000000001","address":"1313 Interiors Parkway","nation":"UNITED STATES"},{"name":"Customer#000000002","address":"1855 Bering Street","nation":"UNITED STATES"},{"name":"Customer#000000003","address":"1135 Cemetery Drive","nation":"UNITED STATES"},{"name":"Customer#000000004","address":"4730 N. Randolph Street","nation":"UNITED STATES"},{"name":"Customer#000000005","address":"1727 Mt. Laurel Avenue","nation":"UNITED STATES"},{"name":"Customer#000000006","address":"5141 Hackett Drive","nation":"UNITED STATES"}]';
WITH customers AS (
    SELECT *
    FROM OPENJSON(@customer_array)
    WITH (
        name VARCHAR(25),
        address VARCHAR(40),
        nation VARCHAR(25),
        customer_id tinyint '$.sql:identity()'
    )
)
SELECT *
FROM customers;
