-- tsql sql:
SELECT DATEDIFF(day, '2007-05-07 09:53:01.0376635', DATEADD(day, 1, SYSDATETIME())) AS OrderDays
FROM (
    VALUES (1), (2), (3)
) AS OrderHeader(OrderID);
