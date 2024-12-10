-- tsql sql:
WITH MessageTypes AS (
    SELECT 'SubmitOrder' AS MessageType, 'WELL_FORMED_XML' AS Validation
    UNION ALL
    SELECT 'OrderShipped', 'WELL_FORMED_XML'
    UNION ALL
    SELECT 'OrderDelivered', 'WELL_FORMED_XML'
),
Contracts AS (
    SELECT 'OrderFulfillment' AS ContractName, 'SubmitOrder' AS MessageType, 'INITIATOR' AS SentBy
    UNION ALL
    SELECT 'OrderFulfillment', 'OrderShipped', 'TARGET'
    UNION ALL
    SELECT 'OrderFulfillment', 'OrderDelivered', 'TARGET'
)
SELECT 'CREATE MESSAGE TYPE [//TPC-H.com/Orders/' + MT.MessageType + '] VALIDATION = ' + MT.Validation + ';' AS MessageTypeQuery,
       'CREATE CONTRACT [//TPC-H.com/Orders/' + C.ContractName + '] ( [//TPC-H.com/Orders/' + C.MessageType + '] SENT BY ' + C.SentBy + ');' AS ContractQuery
FROM MessageTypes MT
CROSS JOIN Contracts C
WHERE MT.MessageType = C.MessageType;
