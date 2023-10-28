SELECT body, REGEXP_SUBSTR(body, '\\b\\S*o\\S*\\b', 3, 3) AS result FROM message;
