-- tsql sql:
SELECT DATEDIFF(day, '2007-05-07 09:53:01.0376635', GETDATE() + 1) AS OrderDays
FROM (
    VALUES (1), (2), (3)
) AS OrderHeader(OrderID);
