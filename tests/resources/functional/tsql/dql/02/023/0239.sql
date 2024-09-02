--Query type: DQL
CREATE PROCEDURE #GET_CONFIG
AS
BEGIN
    SELECT 'config_value' AS config_name, 'config_description' AS config_description;
END;
EXEC #GET_CONFIG;
WITH get_config AS (
    SELECT 'config_value' AS config_name, 'config_description' AS config_description
)
SELECT *
FROM get_config;
-- REMORPH CLEANUP: DROP PROCEDURE #GET_CONFIG;