CREATE TABLE accounts (ID INT, billing_date DATE, balance_due NUMBER(11, 2));

INSERT INTO accounts (ID, billing_date, balance_due) VALUES
    (1, '2018-07-31', 100.00),
    (2, '2018-08-01', 200.00),
    (3, '2018-08-25', 400.00);