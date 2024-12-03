--Query type: DQL
WITH temp_result AS ( SELECT 'allow polybase export' AS config_name, '1' AS config_value UNION ALL SELECT 'allow polybase import', '0' ) SELECT config_name, config_value FROM temp_result WHERE config_name = 'allow polybase export';
