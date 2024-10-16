--Query type: DDL
DECLARE @ResourcePools TABLE (name sysname, max_cpu_percent tinyint, scheduler sysname, max_memory_percent tinyint);
INSERT INTO @ResourcePools (name, max_cpu_percent, scheduler, max_memory_percent)
VALUES ('erp_2', 50, 'EXTERNAL_SCHEDULER', 40);
SELECT *
FROM @ResourcePools
WHERE name = 'erp_2';