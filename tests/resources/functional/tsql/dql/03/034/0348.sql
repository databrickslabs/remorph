-- tsql sql:
SELECT c_customerkey, c_name FROM (VALUES (1, 'Customer1'), (8, 'Customer8'), (12, 'Customer12')) AS Customer(c_customerkey, c_name) WHERE c_customerkey = 1 OR c_customerkey = 8 OR c_customerkey = 12;
