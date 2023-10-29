-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-resource-governor-transact-sql?view=sql-server-ver16

ALTER RESOURCE GOVERNOR WITH (CLASSIFIER_FUNCTION = NULL);  
GO  
ALTER RESOURCE GOVERNOR RECONFIGURE;