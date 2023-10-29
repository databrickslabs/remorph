-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/parse-transact-sql?view=sql-server-ver16

-- The English language is mapped to en-US specific culture  
SET LANGUAGE 'English';  
SELECT PARSE('12/16/2010' AS datetime2) AS Result;