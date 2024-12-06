-- tsql sql:
SELECT RIGHT(c_name, 5) AS [Customer Name] FROM (VALUES ('Customer#000000001', 'Smith'), ('Customer#000000002', 'Johnson'), ('Customer#000000003', 'Williams'), ('Customer#000000004', 'Jones'), ('Customer#000000005', 'Brown')) AS Customer (c_custkey, c_name) WHERE c_custkey < 5 ORDER BY c_name;
