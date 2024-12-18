-- tsql sql:
WITH temp_result AS ( SELECT CAST(l_linenumber AS VARCHAR(10)) AS line_number FROM LINEITEM ) SELECT LTRIM(line_number, '1') AS trimmed_line_number FROM temp_result
