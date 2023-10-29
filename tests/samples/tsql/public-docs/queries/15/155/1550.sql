-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/date-transact-sql?view=sql-server-ver16

DECLARE @date DATE = '12-10-25';
DECLARE @datetime DATETIME = @date;

SELECT @date AS '@date',
    @datetime AS '@datetime';