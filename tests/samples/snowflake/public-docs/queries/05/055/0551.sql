-- see https://docs.snowflake.com/en/sql-reference/functions/approx_percentile

CREATE TABLE testtable (c1 INTEGER);
INSERT INTO testtable (c1) VALUES 
    (0),
    (1),
    (2),
    (3),
    (4),
    (5),
    (6),
    (7),
    (8),
    (9),
    (10);