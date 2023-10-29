-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-route-transact-sql?view=sql-server-ver16

ALTER ROUTE ExpenseRoute  
   WITH   
     SERVICE_NAME = '//Adventure-Works.com/Expenses';