-- see https://docs.snowflake.com/en/sql-reference/functions/system_get_login_failure_details

SELECT JSON_EXTRACT_PATH_TEXT(SYSTEM$GET_LOGIN_FAILURE_DETAILS('0ce9eb56-821d-4ca9-a774-04ae89a0cf5a'), 'errorCode');