-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-pdw-showmaterializedviewoverhead-transact-sql?view=azure-sqldw-latest

CREATE MATERIALIZED VIEW MV1
WITH (DISTRIBUTION = HASH(c1))
AS
SELECT c1, COUNT(*) total_number
FROM dbo.t1 WHERE c1 < 3
GROUP BY c1;