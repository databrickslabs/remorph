-- see https://docs.snowflake.com/en/sql-reference/functions/minhash_combine

CREATE TABLE ta (i INTEGER);
CREATE TABLE tb (i INTEGER);
CREATE TABLE tc (i INTEGER);

-- Insert values into the 3 tables.
INSERT INTO ta (i) VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);
-- Almost the same as the preceding values.
INSERT INTO tb (i) VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (11);
-- Different values and different number of values.
INSERT INTO tc (i) VALUES (-1), (-20), (-300), (-4000);