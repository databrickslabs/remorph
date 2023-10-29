-- see https://docs.snowflake.com/en/sql-reference/sql/create-table-constraint

CREATE TABLE table2 (
    col1 INTEGER NOT NULL,
    col2 INTEGER NOT NULL,
    CONSTRAINT pkey_1 PRIMARY KEY (col1, col2) NOT ENFORCED
    );
CREATE TABLE table3 (
    col_a INTEGER NOT NULL,
    col_b INTEGER NOT NULL,
    CONSTRAINT fkey_1 FOREIGN KEY (col_a, col_b) REFERENCES table2 (col1, col2) NOT ENFORCED
    );