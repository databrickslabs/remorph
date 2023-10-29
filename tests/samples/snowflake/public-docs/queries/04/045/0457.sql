-- see https://docs.snowflake.com/en/sql-reference/functions/to_time

CREATE TABLE demo1_time (
    description VARCHAR,
    value VARCHAR -- yes, string rather than bigint
    );
INSERT INTO demo1_time (description, value) VALUES
   ('Seconds',      '31536001'),
   ('Milliseconds', '31536002400'),
   ('Microseconds', '31536003600000'),
   ('Nanoseconds',  '31536004900000000')
   ;