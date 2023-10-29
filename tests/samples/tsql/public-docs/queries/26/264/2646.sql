-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/json-array-transact-sql?view=sql-server-ver16

SELECT JSON_ARRAY('a', JSON_OBJECT('name':'value', 'type':1))