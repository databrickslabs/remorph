-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-remote-table-as-select-parallel-data-warehouse?view=aps-pdw-2016-au7

SELECT * FROM sys.dm_pdw_dms_workers   
WHERE type = 'PARALLEL_COPY_READER';