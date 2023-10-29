-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/translate-transact-sql?view=sql-server-ver16

SELECT TRANSLATE('2*[3+4]/{7-2}', '[]{}', '()()');