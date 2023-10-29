-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/divide-equals-transact-sql?view=sql-server-ver16

DECLARE @myVariable DECIMAL(5,2);
SET @myVariable = 17.5;
SET @myVariable /= 2;
SELECT @myVariable AS ResultVariable;