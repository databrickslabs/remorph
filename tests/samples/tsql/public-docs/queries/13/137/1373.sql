-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-workload-classifier-transact-sql?view=azure-sqldw-latest

CREATE WORKLOAD CLASSIFIER wgcELTRole
  WITH (WORKLOAD_GROUP = 'staticrc20'
       ,MEMBERNAME = 'ELTRole'
      ,IMPORTANCE = above_normal);