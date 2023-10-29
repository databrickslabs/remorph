-- see https://docs.snowflake.com/en/sql-reference/functions/stddev

CREATE TABLE devious (i INTEGER);
INSERT INTO devious (i) VALUES
    (6),
   (10),
   (14)
   ;

SELECT STDDEV(i) FROM devious;