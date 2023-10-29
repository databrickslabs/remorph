-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/type-id-transact-sql?view=sql-server-ver16

SELECT TYPE_NAME(TYPE_ID('datetime')) AS typeName,   
    TYPE_ID('datetime') AS typeID FROM table1;