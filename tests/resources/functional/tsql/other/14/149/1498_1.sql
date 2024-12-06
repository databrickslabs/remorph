-- tsql sql:
CREATE FUNCTION [dbo].[charindex_s] (@str nvarchar(4000), @search nvarchar(4000))
RETURNS bigint
AS EXTERNAL NAME [SurrogateStringFunction].[Microsoft.Samples.SqlServer.SurrogateStringFunction].[CharindexS];
-- REMORPH CLEANUP: DROP FUNCTION [dbo].[charindex_s];
