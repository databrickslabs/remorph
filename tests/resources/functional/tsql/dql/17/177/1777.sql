--Query type: DQL
DECLARE @customer geometry;
SET @customer = geometry::STMPointFromWKB(0x010400000002000000010100000000000000000059400000000000005940010100000000000000000069400000000000006940, 0);
SELECT @customer.STAsText() AS customer_location;
