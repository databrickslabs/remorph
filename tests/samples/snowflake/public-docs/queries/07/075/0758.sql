-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_substr

SELECT
  '{ "ip_addr":"'
  || REGEXP_SUBSTR (logs,'\\b\\d{1,3}\.\\d{1,3}\.\\d{1,3}\.\\d{1,3}\\b')
  || '", "date":"'
  || REGEXP_SUBSTR (logs,'([\\w:\/]+\\s[+\-]\\d{4})')
  || '", "request":"'
  || REGEXP_SUBSTR (logs,'\"((\\S+) (\\S+) (\\S+))\"', 1, 1, 'e')
  || '", "status":"'
  || REGEXP_SUBSTR (logs,'(\\d{3}) \\d+', 1, 1, 'e')
  || '", "size":"'
  || REGEXP_SUBSTR (logs,'\\d{3} (\\d+)', 1, 1, 'e')
  || '"}' as Apache_HTTP_Server_Access
  FROM log;
