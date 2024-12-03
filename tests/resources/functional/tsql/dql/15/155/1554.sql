--Query type: DQL
DECLARE @date DATETIME = '2011-12-01';
SELECT EOMONTH(dates.date) AS Result
FROM (
    VALUES (@date)
) AS dates (date);
