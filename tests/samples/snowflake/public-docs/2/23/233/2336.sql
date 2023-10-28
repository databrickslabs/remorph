CREATE OR REPLACE TABLE minmax_example(k CHAR(4), d CHAR(4));

INSERT INTO minmax_example VALUES
    ('1', '1'), ('1', '5'), ('1', '3'),
    ('2', '2'), ('2', NULL),
    ('3', NULL),
    (NULL, '7'), (NULL, '1');