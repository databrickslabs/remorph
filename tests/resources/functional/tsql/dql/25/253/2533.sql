-- tsql sql:
SELECT DATENAME(year, o_orderdate) AS order_year, DATENAME(month, o_orderdate) AS order_month, DATENAME(day, o_orderdate) AS order_day, DATENAME(dayofyear, o_orderdate) AS order_dayofyear, DATENAME(weekday, o_orderdate) AS order_weekday FROM (VALUES ('1996-01-02 12:10:30.123')) AS o(o_orderdate);
