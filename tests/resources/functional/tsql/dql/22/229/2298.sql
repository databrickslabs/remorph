--Query type: DQL
WITH temp_result AS (SELECT 'tcp' AS net_transport, 'TCP/IP' AS protocol_type)
SELECT ConnectionProperty('net_transport') AS [Net transport], ConnectionProperty('protocol_type') AS [Protocol type]
FROM temp_result
