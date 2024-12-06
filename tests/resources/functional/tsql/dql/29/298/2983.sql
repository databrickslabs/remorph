-- tsql sql:
SELECT x = SUBSTRING(c_name, 2, 3) FROM (VALUES ('Customer#000000001'), ('Customer#000000002')) AS customers(c_name);
