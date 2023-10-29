-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-service-transact-sql?view=sql-server-ver16

ALTER SERVICE [//Adventure-Works.com/Expenses]  
    (ADD CONTRACT [//Adventure-Works.com/Expenses/ExpenseProcessing],   
     DROP CONTRACT [//Adventure-Works.com/Expenses/ExpenseSubmission]) ;