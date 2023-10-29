-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-rule-transact-sql?view=sql-server-ver16

CREATE RULE pattern_rule   
AS  
@value LIKE '__-%[0-9]'