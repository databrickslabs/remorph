-- tsql sql:
CREATE PROCEDURE sp_wait_for_orders (@seconds int) AS BEGIN DECLARE @time_string nvarchar(8) = '00:00:' + FORMAT(@seconds, 'D2'); WAITFOR DELAY @time_string; WITH orders_cte AS ( SELECT * FROM (VALUES (1, 1001), (2, 500), (3, 2000)) AS orders (id, totalprice) ) SELECT * FROM orders_cte WHERE totalprice > 1000; END; EXEC sp_wait_for_orders 10;
