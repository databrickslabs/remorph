-- tsql sql:
SELECT DATETRUNC(month, DATEADD(month, 4, o_orderdate)) AS order_month FROM (VALUES ('1996-01-02'), ('1996-01-03'), ('1996-01-04')) AS orders (o_orderdate);
