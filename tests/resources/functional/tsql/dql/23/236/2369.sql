-- tsql sql:
WITH temp_result AS ( SELECT * FROM sys.fn_helpcollations() ) SELECT * FROM temp_result WHERE name LIKE 'SQL%';
