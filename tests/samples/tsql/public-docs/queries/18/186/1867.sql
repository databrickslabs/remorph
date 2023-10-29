-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/break-transact-sql?view=sql-server-ver16

DECLARE @sleeptimesec int = 1;
DECLARE @startingtime datetime2(2) = getdate();

PRINT N'Sleeping for ' + CAST(@sleeptimesec as varchar(5)) + ' seconds'
WHILE (1=1)
BEGIN
  
    PRINT N'Sleeping.';  
    PRINT datediff(s, getdate(),  @startingtime)

    IF datediff(s, getdate(),  @startingtime) < -@sleeptimesec
        BEGIN
            PRINT 'We have finished waiting.';
            BREAK;
        END
END