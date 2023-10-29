-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-service-transact-sql?view=sql-server-ver16

CREATE SERVICE [//Adventure-Works.com/Expenses] ON QUEUE ExpenseQueue  
    ([//Adventure-Works.com/Expenses/ExpenseSubmission],  
     [//Adventure-Works.com/Expenses/ExpenseProcessing]) ;