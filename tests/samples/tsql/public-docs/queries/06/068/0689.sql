-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-security-policy-transact-sql?view=sql-server-ver16

ALTER SECURITY POLICY rls.SecPol  
    ALTER BLOCK PREDICATE rls.tenantAccessPredicate_v2(TenantId) 
    ON dbo.Sales AFTER INSERT;