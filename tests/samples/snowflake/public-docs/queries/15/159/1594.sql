-- see https://docs.snowflake.com/en/sql-reference/functions/parse_ip

SELECT column1, PARSE_IP(column1, 'INET') FROM VALUES('192.168.242.188/24'), ('192.168.243.189/24');