-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-route-transact-sql?view=sql-server-ver16

ALTER ROUTE ExpenseRoute  
   WITH   
     BROKER_INSTANCE = 'D8D4D268-00A3-4C62-8F91-634B89B1E317',  
     ADDRESS = 'TCP://www.Adventure-Works.com:1234';