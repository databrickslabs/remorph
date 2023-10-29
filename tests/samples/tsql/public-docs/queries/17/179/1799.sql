-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/scope-resolution-operator-transact-sql?view=sql-server-ver16

DECLARE @hid hierarchyid;  
SELECT @hid = hierarchyid::GetRoot();  
PRINT @hid.ToString();