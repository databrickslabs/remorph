-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/options-transact-sql?view=sql-server-ver16

SET NOCOUNT ON
IF @@OPTIONS & 512 > 0
RAISERROR ('Current user has SET NOCOUNT turned on.', 1, 1)