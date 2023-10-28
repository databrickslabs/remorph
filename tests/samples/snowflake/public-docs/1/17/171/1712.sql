SELECT body, REGEXP_SUBSTR(body, '\\b\\S*o\\S*\\b') AS result FROM message;
