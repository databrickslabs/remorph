--Query type: DML
SELECT * FROM (VALUES (1, 'John', 101, '2020-01-01', 100.00), (2, 'Jane', 102, '2020-01-02', 200.00)) AS CustomerOrders ([CustomerKey], [CustomerName], [OrderKey], [OrderDate], [OrderTotalPrice]);
