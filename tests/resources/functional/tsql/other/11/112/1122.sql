--Query type: DDL
CREATE TABLE #RouteInfo (ServiceName nvarchar(50), Lifetime int, Address nvarchar(50));
INSERT INTO #RouteInfo (ServiceName, Lifetime, Address)
VALUES ('//TPC-H.com/Orders', 259200, 'TCP://services.TPC-H.com:5678');
DECLARE @sql nvarchar(max) = 'CREATE ROUTE OrderRoute WITH SERVICE_NAME = (SELECT ServiceName FROM #RouteInfo), LIFETIME = (SELECT Lifetime FROM #RouteInfo), ADDRESS = (SELECT Address FROM #RouteInfo);';
EXEC sp_executesql @sql;
SELECT * FROM #RouteInfo;
-- REMORPH CLEANUP: DROP TABLE #RouteInfo;
-- REMORPH CLEANUP: DROP ROUTE OrderRoute;