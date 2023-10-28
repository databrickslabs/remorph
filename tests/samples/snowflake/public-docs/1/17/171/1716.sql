SELECT body, REGEXP_SUBSTR(body, '(H\\S*o\\S*\\b).*', 1, 1, '') AS result FROM message;
