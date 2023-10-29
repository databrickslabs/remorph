-- see https://docs.snowflake.com/en/sql-reference/functions/system_get_cmk_akv_consent_url

SELECT SYSTEM$GET_CMK_AKV_CONSENT_URL('my-account' , 'b3ddabe4-e5ed-4e71-8827-0cefb99af240');