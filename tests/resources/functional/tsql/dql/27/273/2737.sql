-- tsql sql:
SELECT RTRIM(c_comment) FROM (VALUES ('Removes trailing spaces.   ')) AS comment(c_comment);