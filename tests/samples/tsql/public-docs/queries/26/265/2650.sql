-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/json-object-transact-sql?view=sql-server-ver16

SELECT JSON_OBJECT('name':'value', 'type':JSON_ARRAY(1, 2))