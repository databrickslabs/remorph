
-- snowflake sql:
SELECT RLIKE('800-456-7891','[2-9]d{2}-d{3}-d{4}') AS matches_phone_number;;

-- databricks sql:
SELECT '800-456-7891' RLIKE '[2-9]d{2}-d{3}-d{4}' AS matches_phone_number;
