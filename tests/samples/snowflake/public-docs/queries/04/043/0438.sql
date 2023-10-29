-- see https://docs.snowflake.com/en/sql-reference/functions/bit_length

CREATE TABLE bl (v VARCHAR, b BINARY);
INSERT INTO bl (v, b) VALUES 
   ('abc', NULL),
   ('\u0394', X'A1B2');