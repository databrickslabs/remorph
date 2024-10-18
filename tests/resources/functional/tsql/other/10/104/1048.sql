--Query type: DDL
SELECT ObjectType, Status FROM (VALUES ('MASTER KEY', 'Created'), ('DATABASE SCOPED CREDENTIAL', 'Created'), ('EXTERNAL DATA SOURCE', 'Created')) AS TempResult (ObjectType, Status);