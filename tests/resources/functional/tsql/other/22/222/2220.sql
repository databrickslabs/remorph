--Query type: DCL
WITH NotificationSubscriptions AS (
    SELECT 73 AS SubscriptionID
)
SELECT 'KILL QUERY NOTIFICATION SUBSCRIPTION ' + CONVERT(VARCHAR, SubscriptionID) AS KillQuery
FROM NotificationSubscriptions;