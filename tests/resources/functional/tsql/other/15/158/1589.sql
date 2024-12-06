-- tsql sql:
WITH conversation AS (
    SELECT 'CustomerClient' AS service_initiator,
           'Orders' AS service_target,
           'OrderSubmission' AS contract_name,
           'current database' AS target
)
SELECT service_initiator,
       service_target,
       contract_name,
       target
FROM conversation;
