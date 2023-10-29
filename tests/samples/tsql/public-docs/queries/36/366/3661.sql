-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/drop-rule-transact-sql?view=sql-server-ver16

sp_unbindrule 'Production.ProductVendor.VendorID'  
DROP RULE VendorID_rule  
GO