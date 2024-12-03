--Query type: DQL
WITH temp_result AS ( SELECT 1 AS id, 'customer' AS type UNION ALL SELECT 2, 'supplier' ) SELECT id, type, DATABASE_PRINCIPAL_ID() AS principal_id FROM temp_result
