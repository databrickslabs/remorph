--Query type: DQL
SELECT DATEPART(year, o_orderdate) AS order_year, DATEPART(month, o_orderdate) AS order_month, DATEPART(day, o_orderdate) AS order_day, DATEPART(dayofyear, o_orderdate) AS order_day_of_year, DATEPART(weekday, o_orderdate) AS order_weekday FROM (VALUES ('1996-01-02')) AS orders (o_orderdate);
