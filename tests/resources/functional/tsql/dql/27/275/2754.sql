--Query type: DQL
SELECT SMALLDATETIMEFROMPARTS(Year, Month, Day, Hour, Minute) AS Result FROM (VALUES (2011, 1, 1, 0, 0)) AS DateParts(Year, Month, Day, Hour, Minute);
