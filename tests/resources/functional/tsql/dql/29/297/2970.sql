--Query type: DQL
WITH CustomerCTE AS (SELECT TOP 10 c_custkey, c_name, c_address FROM Customer),
			OrderCTE AS (SELECT TOP 10 o_orderkey, o_custkey, o_orderstatus FROM Orders),
			LineitemCTE AS (SELECT TOP 10 l_orderkey, l_extendedprice, l_discount FROM Lineitem),
			SupplierCTE AS (SELECT TOP 10 s_suppkey, s_name, s_address FROM Supplier),
			NationCTE AS (SELECT TOP 10 n_nationkey, n_name FROM Nation),
			RegionCTE AS (SELECT TOP 10 r_regionkey, r_name FROM Region)
SELECT c.c_name AS CustomerName,
			o.o_orderstatus AS OrderStatus,
			l.l_extendedprice AS ExtendedPrice,
			s.s_name AS SupplierName,
			n.n_name AS NationName,
			r.r_name AS RegionName
FROM CustomerCTE c
			INNER JOIN OrderCTE o ON c.c_custkey = o.o_custkey
			INNER JOIN LineitemCTE l ON o.o_orderkey = l.l_orderkey
			INNER JOIN SupplierCTE s ON l.l_suppkey = s.s_suppkey
			INNER JOIN NationCTE n ON s.s_nationkey = n.n_nationkey
			INNER JOIN RegionCTE r ON n.n_regionkey = r.r_regionkey
			LEFT JOIN (VALUES (1, 'USA'), (2, 'Canada')) AS Country(country_id, country_name) ON r.r_regionkey = Country.country_id
WHERE c.c_name = 'Customer#000000001' AND o.o_orderstatus = 'O'
ORDER BY l.l_extendedprice;
