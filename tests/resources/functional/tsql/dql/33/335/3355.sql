-- tsql sql:
SELECT c_last_name, c_first_name FROM (VALUES ('Russell', 'John'), ('Rogers', 'Mike'), ('Robinson', 'Tom'), ('Reynolds', 'Bob'), ('Richardson', 'Alice')) AS Customer (c_last_name, c_first_name) WHERE c_last_name LIKE 'R%' ORDER BY c_first_name ASC, c_last_name DESC;
