--Query type: DQL
DECLARE @Date VARCHAR(50) = '2009-05-12 10:19:41.177';
IF ISDATE(@Date) = 1
    SELECT 'DATE IS VALID';
ELSE
    SELECT 'DATE IS INVALID';
