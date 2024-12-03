--Query type: DQL
WITH CustomerCTE AS (SELECT * FROM (VALUES (1, 'Customer1'), (2, 'Customer2')) AS Customer(c_custkey, c_name)),
OrderCTE AS (SELECT * FROM (VALUES (1, 1, 'Order1'), (2, 1, 'Order2')) AS Orders(o_orderkey, o_custkey, o_orderstatus)),
OrderLineCTE AS (SELECT COUNT(*) AS ol_count FROM (VALUES (1, 1, 1), (2, 1, 2)) AS OrderLine(ol_orderkey, ol_custkey, ol_linenumber))
SELECT * FROM CustomerCTE
INNER JOIN OrderCTE
    ON CustomerCTE.c_custkey = OrderCTE.o_custkey
    AND OrderCTE.o_orderkey = (SELECT ol_count FROM OrderLineCTE)
