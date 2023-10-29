-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/graph-id-from-edge-id-transact-sql?view=sql-server-ver16

SELECT GRAPH_ID_FROM_EDGE_ID($edge_id)
FROM friendOf;