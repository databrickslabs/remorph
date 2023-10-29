-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/copy-into-transact-sql?view=azure-sqldw-latest

GRANT ADMINISTER DATABASE BULK OPERATIONS to [mike@contoso.com];
GRANT INSERT to [mike@contoso.com];

GRANT CREATE TABLE to [mike@contoso.com];
GRANT ALTER on SCHEMA::HR to [mike@contoso.com];