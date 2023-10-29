-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16

SELECT DATETRUNC(month, '1998-03-04');

SELECT DATETRUNC(millisecond, '1998-03-04 10:10:05.1234567');

DECLARE @d1 char(200) = '1998-03-04';
SELECT DATETRUNC(millisecond, @d1);

DECLARE @d2 nvarchar(max) = '1998-03-04 10:10:05';
SELECT DATETRUNC(minute, @d2);