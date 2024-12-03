--Query type: DML
WITH ServiceInfo AS (
    SELECT 'CustomerService' AS ServiceName, 'CustomerContract' AS ContractName, 'CustomerQueue' AS QueueName
    UNION ALL
    SELECT 'Orders', 'OrdersContract', 'OrdersQueue'
)
SELECT *
FROM ServiceInfo;
