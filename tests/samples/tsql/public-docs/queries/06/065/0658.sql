-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-message-type-transact-sql?view=sql-server-ver16

ALTER MESSAGE TYPE  
    [//Adventure-Works.com/Expenses/SubmitExpense]  
    VALIDATION = WELL_FORMED_XML ;