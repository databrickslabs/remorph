
-- snowflake sql:
SELECT ENDSWITH(COLLATE('ñn', 'sp'), COLLATE('n', 'sp'));

-- databricks sql:
SELECT ENDSWITH(COLLATE('ñn', 'sp'), COLLATE('n', 'sp'));
