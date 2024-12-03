--Query type: DDL
CREATE PROCEDURE dbo.LengthProcedure (@string_exp NVARCHAR(4000))
AS
SELECT {fn BIT_LENGTH(@string_exp)} AS Length
FROM (VALUES (@string_exp)) AS temp_table(string_exp);
