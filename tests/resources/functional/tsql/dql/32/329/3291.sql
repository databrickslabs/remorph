--Query type: DQL
DECLARE @region CHAR(25);
SET @region = N'ASIA';

WITH Customer AS (
    SELECT RTRIM(c_name) + ' ' + RTRIM(c_address) AS Name, c_city
    FROM (
        VALUES ('Customer#000000001', '1297.35.99120', 'DELHI'),
               ('Customer#000000002', '1297.35.99121', 'MUMBAI'),
               ('Customer#000000003', '1297.35.99122', 'CHENNAI')
    ) AS Customer (c_name, c_address, c_city)
)

SELECT Name, c_city
FROM Customer
WHERE c_city = @region;