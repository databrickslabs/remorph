
-- snowflake sql:
SELECT BASE64_DECODE_STRING(BASE64_ENCODE('HELLO')), TRY_BASE64_DECODE_STRING(BASE64_ENCODE('HELLO'));

-- databricks sql:
SELECT UNBASE64(BASE64('HELLO')), UNBASE64(BASE64('HELLO'));
