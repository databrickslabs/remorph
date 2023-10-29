-- see https://docs.snowflake.com/en/sql-reference/sql/delete

INSERT INTO leased_bicycles (bicycle_ID, customer_ID) VALUES
    (101, 1111),
    (102, 2222),
    (103, 3333),
    (104, 4444),
    (105, 5555);
INSERT INTO returned_bicycles (bicycle_ID) VALUES
    (102),
    (104);