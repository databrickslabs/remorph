-- tsql sql:
WITH temp_result AS ( SELECT 'P' AS char1, 'æ' AS char2 ) SELECT ASCII(char1) AS [ASCII], ASCII(char2) AS [Extended_ASCII] FROM temp_result;
