-- tsql sql:
WITH temp_result AS ( SELECT DB_NAME() AS current_database ) SELECT current_database FROM temp_result;
