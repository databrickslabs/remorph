-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/coalesce-transact-sql?view=sql-server-ver16

USE tempdb;  
GO  
-- This statement fails because the PRIMARY KEY cannot accept NULL values  
-- and the nullability of the COALESCE expression for col2   
-- evaluates to NULL.  
CREATE TABLE #Demo   
(   
  col1 INTEGER NULL,   
  col2 AS COALESCE(col1, 0) PRIMARY KEY,   
  col3 AS ISNULL(col1, 0)   
);   

-- This statement succeeds because the nullability of the   
-- ISNULL function evaluates AS NOT NULL.  

CREATE TABLE #Demo   
(   
  col1 INTEGER NULL,   
  col2 AS COALESCE(col1, 0),   
  col3 AS ISNULL(col1, 0) PRIMARY KEY   
);