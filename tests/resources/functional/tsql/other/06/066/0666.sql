--Query type: DML
CREATE TABLE calendar (c_date DATE);
INSERT INTO calendar (c_date)
VALUES
    ('2015-01-01'),
    ('2015-01-02'),
    ('2015-01-03'),
    ('2015-01-04'),
    ('2015-01-05'),
    ('2015-01-06'),
    ('2015-01-07'),
    ('2015-01-08');
SELECT * FROM calendar;
-- REMORPH CLEANUP: DROP TABLE calendar;