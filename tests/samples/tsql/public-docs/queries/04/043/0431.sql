-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-table-index-option-transact-sql?view=sql-server-ver16

--For rowstore tables  
REBUILD WITH   
(  
  DATA_COMPRESSION = NONE ON PARTITIONS (1),   
  DATA_COMPRESSION = ROW ON PARTITIONS (2, 4, 6 TO 8),   
  DATA_COMPRESSION = PAGE ON PARTITIONS (3, 5)  
)  
  
--For columnstore tables  
REBUILD WITH   
(  
  DATA_COMPRESSION = COLUMNSTORE ON PARTITIONS (1, 3, 5),   
  DATA_COMPRESSION = COLUMNSTORE_ARCHIVE ON PARTITIONS (2, 4, 6 TO 8)  
)