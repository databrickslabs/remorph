-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

SELECT CAST('<Name><FName>Carol</FName><LName>Elliot</LName></Name>'  AS XML)