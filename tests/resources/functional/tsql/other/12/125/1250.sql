-- tsql sql:
CREATE TABLE #Orders ([o_orderdate] DATE, [o_orderkey] INT, [o_custkey] INT, [o_totalprice] DECIMAL(10, 2));
INSERT INTO #Orders ([o_orderdate], [o_orderkey], [o_custkey], [o_totalprice])
VALUES ('1992-01-01', 1, 1, 100.0), ('1992-01-02', 2, 2, 200.0), ('1992-01-03', 3, 3, 300.0);
CREATE TABLE [dbo].[Orders_out]
WITH (DISTRIBUTION = HASH([o_orderkey]))
AS
SELECT [o_orderdate], [o_orderkey], [o_custkey], [o_totalprice], [o_totalprice]*0.1 AS [discount],
CASE WHEN [o_totalprice] > 10000 THEN 'High' ELSE 'Low' END AS [order_priority]
FROM #Orders
OPTION (LABEL = 'CTAS : Partition OUT table : Create');
SELECT * FROM [dbo].[Orders_out];
