-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/collations?view=sql-server-ver16

SELECT name, description
FROM fn_helpcollations();