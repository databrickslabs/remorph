-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-server-audit-specification-transact-sql?view=sql-server-ver16

CREATE SERVER AUDIT SPECIFICATION HIPAA_Audit_Specification  
FOR SERVER AUDIT HIPAA_Audit  
    ADD (FAILED_LOGIN_GROUP)  
    WITH (STATE=ON);  
GO