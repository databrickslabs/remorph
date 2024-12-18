-- tsql sql:
WITH OrderDates AS ( SELECT MIN(OrderDate) AS MinOrderDate, MAX(OrderDate) AS MaxOrderDate FROM ( VALUES ('2022-01-01'), ('2022-01-31') ) AS OrderDateTable(OrderDate) ) SELECT DATEDIFF(day, MinOrderDate, MaxOrderDate) FROM OrderDates
