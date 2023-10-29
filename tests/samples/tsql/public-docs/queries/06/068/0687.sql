-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-security-policy-transact-sql?view=sql-server-ver16

ALTER SECURITY POLICY pol1   
    ADD FILTER PREDICATE schema_preds.SecPredicate(column1)   
    ON myschema.mytable;