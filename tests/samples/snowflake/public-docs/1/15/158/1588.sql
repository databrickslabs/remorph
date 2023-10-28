CREATE TABLE home_sales (
    sale_date DATE,
    price NUMBER(11, 2)
    );
INSERT INTO home_sales (sale_date, price) VALUES 
    ('2013-08-01'::DATE, 290000.00),
    ('2014-02-01'::DATE, 320000.00),
    ('2015-04-01'::DATE, 399999.99),
    ('2016-04-01'::DATE, 400000.00),
    ('2017-04-01'::DATE, 470000.00),
    ('2018-04-01'::DATE, 510000.00);