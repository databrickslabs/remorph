--Query type: DQL
IF 3 < SOME (SELECT order_total FROM (VALUES (10.0), (20.0), (30.0)) AS order_values(order_total))
    PRINT 'TRUE'
ELSE
    PRINT 'FALSE';