-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/patindex-transact-sql?view=sql-server-ver16

SELECT position = PATINDEX('%en_ure%', 'Please ensure the door is locked!');