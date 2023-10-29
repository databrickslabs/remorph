-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/bitwise-not-transact-sql?view=sql-server-ver16

CREATE TABLE bitwise (  
  a_int_value INT NOT NULL,  
  b_int_value INT NOT NULL); 
GO  
INSERT bitwise VALUES (170, 75);  
GO