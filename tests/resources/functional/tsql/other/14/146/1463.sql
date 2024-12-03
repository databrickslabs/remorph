--Query type: DML
DECLARE @ID NVARCHAR(max);
WITH TempData AS (
    SELECT N'0E984725-C51C-4BF4-9960-E1C80E27ABA0wrong' AS ID
)
SELECT @ID = ID FROM TempData;
SELECT @ID AS OriginalValue, CONVERT(uniqueidentifier, @ID) AS ConvertedValue;
