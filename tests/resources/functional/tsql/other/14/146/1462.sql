--Query type: DML
DECLARE @ID NVARCHAR(max) = N'0E984725-C51C-4BF4-9960-E1C80E27ABA0';
SELECT ID, CONVERT(uniqueidentifier, ID) AS TruncatedValue
FROM (VALUES (@ID)) AS id_table(ID);