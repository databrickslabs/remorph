-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-rule-transact-sql?view=sql-server-ver16

CREATE RULE range_rule  
AS   
@range>= $1000 AND @range <$20000;