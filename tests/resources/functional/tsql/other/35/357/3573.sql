--Query type: DCL
WITH temp_result AS ( SELECT 'JanethEsteves' AS username ) SELECT 'REVOKE SELECT ON OBJECT::dbo.customer FROM ' + username + ';' AS revoke_statement FROM temp_result;