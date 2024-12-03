--Query type: DQL
WITH temp_result AS (
    SELECT N'customer' AS table_name
)
SELECT OBJECT_ID(N'tpc_h.dbo.' + table_name) AS [Object ID]
FROM temp_result;
