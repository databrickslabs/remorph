-- tsql sql:
WITH temp_product AS (SELECT DISTINCT p_name, p_id FROM (VALUES ('Long-Sleeve Logo Jersey', 1), ('Long-Sleeve Logo Jersey', 2)) AS p (p_name, p_id)), temp_product_model AS (SELECT DISTINCT pm_id, pm_name FROM (VALUES (1, 'Long-Sleeve Logo Jersey'), (2, 'Long-Sleeve Logo Jersey')) AS pm (pm_id, pm_name)) SELECT DISTINCT tp.p_name FROM temp_product tp WHERE tp.p_id IN (SELECT tpm.pm_id FROM temp_product_model tpm WHERE tp.p_id = tpm.pm_id AND tpm.pm_name LIKE 'Long-Sleeve Logo Jersey%');
