-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

DECLARE @d1 DATE, @dt1 DATETIME , @dt2 DATETIME2

SET @d1 = '1492-08-03'
--This is okay; Minimum YYYY for DATE is 0001

SET @dt2 = CAST(@d1 AS DATETIME2)
--This is okay; Minimum YYYY for DATETIME2 IS 0001

SET @dt1 = CAST(@d1 AS DATETIME)
--This will error with (Msg 242) "The conversion of a date data type to a datetime data type resulted in an out-of-range value."
--Minimum YYYY for DATETIME is 1753