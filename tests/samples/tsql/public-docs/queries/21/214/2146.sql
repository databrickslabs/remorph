-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/trigger-nestlevel-transact-sql?view=sql-server-ver16

IF ( (SELECT trigger_nestlevel() ) > 5 )  
   RAISERROR  
      ('This statement nested over 5 levels of triggers.',16,-1)