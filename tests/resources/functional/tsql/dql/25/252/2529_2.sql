--Query type: DQL
WITH dates AS ( SELECT '2005-12-31 23:59:59.9999999' AS date1, '2006-01-01 00:00:00.0000000' AS date2 ) SELECT DATEDIFF(dayofyear, date1, date2) FROM dates