--Query type: DML
INSERT INTO regions (region_ID, name)
SELECT region_ID, name
FROM (
    VALUES (1, 'North America'),
           (2, 'South America'),
           (3, 'Europe'),
           (4, 'Asia'),
           (5, 'Africa')
) AS regions (region_ID, name);