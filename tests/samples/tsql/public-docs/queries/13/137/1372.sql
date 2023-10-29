-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-workload-classifier-transact-sql?view=azure-sqldw-latest

CREATE WORKLOAD CLASSIFIER wcELTLoads WITH  
( WORKLOAD_GROUP = 'wgDataLoads'
 ,MEMBERNAME     = 'ELTRole'  
 ,START_TIME     = '22:00'
 ,END_TIME       = '02:00' )