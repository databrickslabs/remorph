-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/object-id-from-node-id-transact-sql?view=sql-server-ver16

SELECT OBJECT_ID_FROM_NODE_ID($from_id)
FROM likes;