-- tsql sql:
WITH SalesPersonCTE AS ( SELECT o_orderpriority, SUM(l_extendedprice) AS TotalRevenue FROM lineitem GROUP BY o_orderpriority ) SELECT o_orderpriority, TotalRevenue, GROUPING(o_orderpriority) AS [Grouping] FROM SalesPersonCTE GROUP BY o_orderpriority WITH ROLLUP;
