-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/deallocate-transact-sql?view=sql-server-ver16

DECLARE abc SCROLL CURSOR FOR  
SELECT * FROM Person.Person;