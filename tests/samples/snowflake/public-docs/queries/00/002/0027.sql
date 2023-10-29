-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_substr

-- Prepare example
CREATE OR REPLACE TABLE log (logs varchar);

INSERT INTO log (logs) VALUES
('127.0.0.1 - - [10/Jan/2018:16:55:36 -0800] "GET / HTTP/1.0" 200 2216'),
('192.168.2.20 - - [14/Feb/2018:10:27:10 -0800] "GET /cgi-bin/try/ HTTP/1.0" 200 3395');