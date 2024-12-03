--Query type: DQL
SELECT IIF(DATENAME(weekday, Date) IN ('Saturday', 'Sunday'), 'Weekend', 'Weekday') AS CurrentDay FROM (VALUES(GETDATE())) AS DateTable(Date);
