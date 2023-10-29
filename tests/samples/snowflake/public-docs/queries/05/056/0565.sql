-- see https://docs.snowflake.com/en/sql-reference/functions/regr_valx

CREATE TABLE xy (col_x DOUBLE, col_y DOUBLE);
INSERT INTO xy (col_x, col_y) VALUES
    (1.0, 2.0),
    (3.0, NULL),
    (NULL, 6.0);