--Query type: DQL
DECLARE @OrderIDVariable INT;

WITH OrdersCTE AS (
  SELECT OrderID, CustomerID, OrderDate
  FROM (
    VALUES (1, 1, '2020-01-01'),
           (2, 2, '2020-01-02'),
           (3, 3, '2020-01-03')
  ) AS Orders(OrderID, CustomerID, OrderDate)
)

SELECT @OrderIDVariable = MAX(OrderID)
FROM OrdersCTE;
