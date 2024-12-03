--Query type: DQL
SELECT c_name, c_address, o_orderdate AS FirstOrderDate FROM (VALUES ('Customer1', 'Address1', '2020-01-01'), ('Customer2', 'Address2', '2020-01-15'), ('Customer3', 'Address3', '2020-02-01')) AS CustomerOrders (c_name, c_address, o_orderdate) ORDER BY c_name;
