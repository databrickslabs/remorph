-- tsql sql:
SELECT COUNT(*) FROM (VALUES ('2013-12-30'), ('2013-12-29'), ('2013-12-28')) AS OrderDateTable(OrderDate) WHERE OrderDate < '2013-12-31';
