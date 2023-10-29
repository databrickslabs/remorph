-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/translate-transact-sql?view=sql-server-ver16

SELECT TRANSLATE('abcdef','abc','bcd') AS Translated,
       REPLACE(REPLACE(REPLACE('abcdef','a','b'),'b','c'),'c','d') AS Replaced;