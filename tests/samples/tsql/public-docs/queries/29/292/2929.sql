-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-resource-pool-transact-sql?view=sql-server-ver16

SELECT osn.memory_node_id AS [numa_node_id], sc.cpu_id, sc.scheduler_id  
FROM sys.dm_os_nodes AS osn  
INNER JOIN sys.dm_os_schedulers AS sc 
   ON osn.node_id = sc.parent_node_id 
      AND sc.scheduler_id < 1048576;