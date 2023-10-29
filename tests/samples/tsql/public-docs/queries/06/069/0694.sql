-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-server-audit-specification-transact-sql?view=sql-server-ver16

ALTER SERVER AUDIT SPECIFICATION HIPAA_Audit_Specification  
FOR SERVER AUDIT HIPAA_Audit  
    DROP (FAILED_LOGIN_GROUP),  
    ADD (DATABASE_OBJECT_ACCESS_GROUP)  
    WITH (STATE=ON);  
GO