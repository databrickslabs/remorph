-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

SELECT CONVERT(XML, '<root>          <child/>         </root>', 1)