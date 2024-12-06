-- tsql sql:
SELECT CONCAT_WS(',', c_name, NULL, NULL, c_address, c_city, c_phone) AS CustomerInfo FROM (VALUES ('Customer#000000001', '1297.35.99135', '77191', '25-989-741-2988')) AS Customer(c_name, c_address, c_city, c_phone);
