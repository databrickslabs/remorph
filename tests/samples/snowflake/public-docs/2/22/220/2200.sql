CREATE OR REPLACE TABLE bitwise_example
        (k int, d decimal(10,5), s1 varchar(10), s2 varchar(10));

INSERT INTO bitwise_example VALUES
        (15, 1.1, '12','one'),
        (26, 2.9, '10','two'),
        (12, 7.1, '7.9','two'),
        (14, null, null,'null'),
        (8, null, null, 'null'),
        (null, 9.1, '14','nine');