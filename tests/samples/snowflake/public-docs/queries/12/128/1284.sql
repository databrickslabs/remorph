-- see https://docs.snowflake.com/en/sql-reference/functions/parse_ip

SELECT PARSE_IP('fe80::20c:29ff:fe2c:429/64', 'INET');
