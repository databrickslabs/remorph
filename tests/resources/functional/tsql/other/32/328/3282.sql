--Query type: DDL
CREATE AGGREGATE CalculateTotal (@input decimal(18, 2)) RETURNS decimal(18, 2) EXTERNAL NAME [TPCHUtilities].[Microsoft.Samples.SqlServer.CalculateTotal];