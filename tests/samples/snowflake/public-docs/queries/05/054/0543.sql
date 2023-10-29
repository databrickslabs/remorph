-- see https://docs.snowflake.com/en/sql-reference/functions/conditional_true_event

CREATE TABLE table1 (province VARCHAR, o_col INTEGER, o2_col INTEGER);
INSERT INTO table1 (province, o_col, o2_col) VALUES
    ('Alberta',    0, 10),
    ('Alberta',    0, 10),
    ('Alberta',   13, 10),
    ('Alberta',   13, 11),
    ('Alberta',   14, 11),
    ('Alberta',   15, 12),
    ('Alberta', NULL, NULL),
    ('Manitoba',    30, 30);