-- see https://docs.snowflake.com/en/sql-reference/functions/to_date

CREATE TABLE demo1 (
    description VARCHAR,
    value VARCHAR -- yes, string rather than bigint
    );

INSERT INTO demo1 (description, value) VALUES
   ('Seconds',      '31536000'),
   ('Milliseconds', '31536000000'),
   ('Microseconds', '31536000000000'),
   ('Nanoseconds',  '31536000000000000')
   ;