--Query type: DDL
DECLARE @NewOrderQueue TABLE (MessageBody varbinary(max));

DECLARE @NewOrderRequestMessage sysname = 'NewOrderRequest';
DECLARE @NewOrderResponseMessage sysname = 'NewOrderResponse';

DECLARE @NewOrderContract sysname = 'NewOrderContract';

DECLARE @ServiceName sysname = '[//TPC-H.com/Orders]';
DECLARE @QueueName sysname = 'NewOrderQueue';

DECLARE @RouteName sysname = 'RouteToTPCH';
DECLARE @ServiceAddress nvarchar(256) = '//TPC-H.com/Orders';
DECLARE @RouteAddress nvarchar(256) = 'LOCAL';

-- CREATE QUEUE NewOrderQueue;
-- CREATE SERVICE [@ServiceName] ON QUEUE NewOrderQueue (NewOrderContract);
-- CREATE ROUTE @RouteName WITH SERVICE @ServiceAddress, ADDRESS @RouteAddress;

SELECT 'Temporary table and variables created successfully.' AS Message;

-- REMORPH CLEANUP: DROP TABLE @NewOrderQueue;
-- REMORPH CLEANUP: DROP SERVICE [@ServiceName];
-- REMORPH CLEANUP: DROP ROUTE @RouteName;
-- REMORPH CLEANUP: DROP CONTRACT @NewOrderContract;
-- REMORPH CLEANUP: DROP MESSAGE TYPE @NewOrderResponseMessage;
-- REMORPH CLEANUP: DROP MESSAGE TYPE @NewOrderRequestMessage;
