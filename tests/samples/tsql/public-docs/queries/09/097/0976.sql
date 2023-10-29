-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=sql-server-ver16

CREATE EXTERNAL DATA SOURCE [DataSource_SQLInstanceListener_ReadOnlyIntent]
WITH (
  LOCATION = 'sqlserver://WINSQL2019AGL' ,
  CONNECTION_OPTIONS = 'ApplicationIntent=ReadOnly' ,
  CREDENTIAL = [SQLServerCredentials]);
GO
CREATE EXTERNAL DATA SOURCE [DataSource_SQLInstanceListener_ReadWriteIntent]
WITH (
  LOCATION = 'sqlserver://WINSQL2019AGL' ,
  CONNECTION_OPTIONS = 'ApplicationIntent=ReadWrite' ,
  CREDENTIAL = [SQLServerCredentials]);
GO