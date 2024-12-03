--Query type: DDL
SELECT * FROM ( VALUES ('erp_1', 50, 40), ('erp_2', 60, 50) ) AS ResourcePools(ResourcePoolName, MAX_CPU_PERCENT, MAX_MEMORY_PERCENT);
