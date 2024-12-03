--Query type: DQL
DECLARE @t datetime = '1999-01-01';
SELECT DATENAME(year, @t) AS order_year;
