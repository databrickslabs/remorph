-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/graph-id-from-node-id-transact-sql?view=sql-server-ver16

SELECT GRAPH_ID_FROM_NODE_ID($node_id)
FROM Person;