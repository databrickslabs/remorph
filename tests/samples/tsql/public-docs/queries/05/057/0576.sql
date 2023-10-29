-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-external-data-source-transact-sql?view=sql-server-ver16

ALTER EXTERNAL DATA SOURCE hadoop_eds SET
   CREDENTIAL = new_hadoop_user
    ;