-- see https://docs.snowflake.com/en/sql-reference/functions/greatest

CREATE TABLE test_table_1_greatest (col_1 INTEGER, col_2 INTEGER, 
    col_3 INTEGER, col_4 FLOAT);
INSERT INTO test_table_1_greatest (col_1, col_2, col_3, col_4) VALUES
    (1, 2,    3,  4.00),
    (2, 4,   -1, -2.00),
    (3, 6, NULL, 13.45);