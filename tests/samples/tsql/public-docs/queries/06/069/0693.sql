-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-server-audit-transact-sql?view=sql-server-ver16

ALTER SERVER AUDIT HIPAA_Audit  
WITH (STATE = OFF);    
GO  
DROP SERVER AUDIT HIPAA_Audit;  
GO