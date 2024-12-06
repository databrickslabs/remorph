-- tsql sql:
SELECT l_name, c_name, o_totalprice FROM (VALUES ('Smith', 'Customer#000000001', 100.00), ('Johnson', 'Customer#000000002', 200.00)) AS Customer (l_name, c_name, o_totalprice);
