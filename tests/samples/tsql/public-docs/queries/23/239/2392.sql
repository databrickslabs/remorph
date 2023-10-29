-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/options-transact-sql?view=sql-server-ver16

SELECT @@OPTIONS AS OriginalOptionsValue;
SET CONCAT_NULL_YIELDS_NULL OFF;
SELECT 'abc' + NULL AS ResultWhen_OFF, @@OPTIONS AS OptionsValueWhen_OFF;
  
SET CONCAT_NULL_YIELDS_NULL ON;
SELECT 'abc' + NULL AS ResultWhen_ON, @@OPTIONS AS OptionsValueWhen_ON;