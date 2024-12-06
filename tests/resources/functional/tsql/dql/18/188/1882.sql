-- tsql sql:
SELECT DATALENGTH(column1) AS bit_length, DATALENGTH(column1) AS octet_length, CONCAT('CONCAT ', 'returns a character string') AS concat_result, CONVERT(DECIMAL(10, 4), 100.123456) AS truncate_result, CONVERT(date, GETDATE()) AS current_date_value, CONVERT(time(6), GETDATE()) AS current_time_value FROM (VALUES ('Returns the length.')) AS temp_result(column1)
