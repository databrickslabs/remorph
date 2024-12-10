-- tsql sql:
SELECT INDEXPROPERTY(OBJECT_ID('temp_result'), 'PK_temp_result', 'IsClustered') AS [Is Clustered],
       INDEXPROPERTY(OBJECT_ID('temp_result'), 'PK_temp_result', 'IndexDepth') AS [Index Depth],
       INDEXPROPERTY(OBJECT_ID('temp_result'), 'PK_temp_result', 'IndexFillFactor') AS [Fill Factor]
FROM (
    VALUES (1, 'name', 'address')
) AS temp_result (c_custkey, c_name, c_address);
