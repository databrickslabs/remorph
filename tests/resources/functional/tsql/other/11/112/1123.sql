--Query type: DDL
DECLARE @Routes TABLE (RouteName sysname, ServiceName nvarchar(255), BrokerInstance uniqueidentifier, Address nvarchar(255));
INSERT INTO @Routes (RouteName, ServiceName, BrokerInstance, Address)
VALUES ('SalesRoute', '//TPC-H.com/Sales', '12345678-1234-1234-1234-123456789012', 'TCP://SERVER01:5678');
SELECT * FROM @Routes;
