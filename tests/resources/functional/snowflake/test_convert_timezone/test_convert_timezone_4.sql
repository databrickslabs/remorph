
-- source:
SELECT CURRENT_TIMESTAMP() AS now_in_la,
                CONVERT_TIMEZONE('America/New_York', CURRENT_TIMESTAMP()) AS now_in_nyc,
                CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP()) AS now_in_paris,
                CONVERT_TIMEZONE('Asia/Tokyo', CURRENT_TIMESTAMP()) AS now_in_tokyo;

-- databricks_sql:
SELECT
        CURRENT_TIMESTAMP() AS now_in_la, CONVERT_TIMEZONE('America/New_York', CURRENT_TIMESTAMP()) AS now_in_nyc,
        CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP()) AS now_in_paris,
        CONVERT_TIMEZONE('Asia/Tokyo', CURRENT_TIMESTAMP()) AS now_in_tokyo;
