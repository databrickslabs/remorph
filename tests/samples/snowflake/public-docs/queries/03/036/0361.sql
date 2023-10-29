-- see https://docs.snowflake.com/en/sql-reference/functions/sum

CREATE OR REPLACE TABLE sum_example(k INT, d DECIMAL(10,5),
                                    s1 VARCHAR(10), s2 VARCHAR(10));

INSERT INTO sum_example VALUES
(1, 1.1, '1.1','one'), (1, 10, '10','ten'),
(2, 2.2, '2.2','two'), (2, null, null,'null'),
(3, null, null, 'null'),
(null, 9, '9.9','nine');

SELECT * FROM sum_example;


SELECT SUM(d), SUM(s1) FROM sum_example;


select k, SUM(d), SUM(s1) FROM sum_example GROUP BY k;


SELECT SUM(s2) FROM sum_example;

100038 (22018): Numeric value 'one' is not recognized