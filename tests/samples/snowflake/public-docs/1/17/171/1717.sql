SELECT body, REGEXP_SUBSTR(body, '(H\\S*o\\S*\\b) .*', 1, 1, 'e') AS result FROM message;
