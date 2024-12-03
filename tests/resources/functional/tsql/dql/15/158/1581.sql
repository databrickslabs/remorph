--Query type: DQL
DECLARE @days INT = 365, @datetime DATETIME2 = '1995-01-01 01:01:01.1110000';
SELECT DATE_BUCKET(DAY, @days, @datetime) AS bucketed_date
FROM (VALUES (@datetime)) AS dates (date_value);
