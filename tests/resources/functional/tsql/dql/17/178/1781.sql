--Query type: DQL
DECLARE @customer geometry;
SET @customer = geometry::STPolyFromWKB(0x0103000000010000000400000000000000000014400000000000001440000000000000244000000000000014400000000000002440000000000000244000000000000014400000000000001440, 0);
SELECT c_name, c_address, @customer.STAsText() AS customer_location
FROM (
    VALUES ('Customer1', '123 Main St'),
           ('Customer2', '456 Elm St')
) AS customers (c_name, c_address);