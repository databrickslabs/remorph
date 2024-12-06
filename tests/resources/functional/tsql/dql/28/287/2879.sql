-- tsql sql:
SELECT c.* FROM (VALUES ('Customer1', 1), ('Customer2', 2), ('Customer3', 3)) AS c (CustomerName, CustomerId);
