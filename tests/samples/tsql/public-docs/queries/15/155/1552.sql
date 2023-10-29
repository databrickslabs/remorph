-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/date-transact-sql?view=sql-server-ver16

DECLARE @date DATE = '1912-10-25';
DECLARE @datetimeoffset DATETIMEOFFSET(3) = @date;

SELECT @date AS '@date',
    @datetimeoffset AS '@datetimeoffset';