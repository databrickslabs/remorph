--Query type: DQL
SELECT *
FROM OPENROWSET(BULK N'D:\XChange\test-csv.csv', FORMATFILE = N'D:\XChange\test-csv.fmt', FIRSTROW = 2, FORMAT = 'CSV') AS cars
WHERE price > 150;
