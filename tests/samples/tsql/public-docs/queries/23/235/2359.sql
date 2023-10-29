-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/grant-system-object-permissions-transact-sql?view=sql-server-ver16

SELECT * FROM master.sys.database_permissions AS dp   
    JOIN sys.system_objects AS so  
    ON dp.major_id = so.object_id  
    WHERE dp.class = 1 AND so.parent_object_id = 0 ;  
GO