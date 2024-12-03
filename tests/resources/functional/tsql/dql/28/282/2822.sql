--Query type: DQL
WITH temp_result AS ( SELECT '     test    ' AS str ) SELECT TRIM(str) AS Result FROM temp_result;
