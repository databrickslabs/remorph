-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/date-transact-sql?view=sql-server-ver16

DECLARE @date DATE = '1912-10-25';
DECLARE @smalldatetime SMALLDATETIME = @date;

SELECT @date AS '@date',
    @smalldatetime AS '@smalldatetime';