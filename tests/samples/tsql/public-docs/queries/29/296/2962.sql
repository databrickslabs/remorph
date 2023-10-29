-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-sequence-transact-sql?view=sql-server-ver16

SELECT sch.name + '.' + seq.name AS [Sequence schema and name]   
    FROM sys.sequences AS seq  
    JOIN sys.schemas AS sch  
        ON seq.schema_id = sch.schema_id ;  
GO