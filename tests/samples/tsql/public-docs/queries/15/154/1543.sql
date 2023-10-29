-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/datetrunc-transact-sql?view=sql-server-ver16

DECLARE @d datetime2 = '2021-11-11 11:11:11.1234567';

SELECT 'Week-7', DATETRUNC(week, @d); -- Uses the default DATEFIRST setting value of 7 (U.S. English)

SET DATEFIRST 6;
SELECT 'Week-6', DATETRUNC(week, @d);

SET DATEFIRST 3;
SELECT 'Week-3', DATETRUNC(week, @d);