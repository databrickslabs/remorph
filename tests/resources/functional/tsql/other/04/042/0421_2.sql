--Query type: DML
INSERT INTO #supplier (supplier_id, supplier_name)
SELECT supplier_id, supplier_name
FROM (
    VALUES (1, 'Supplier1'),
           (2, 'Supplier2'),
           (3, 'Supplier3'),
           (4, 'Supplier4'),
           (5, 'Supplier5')
) AS supplier (supplier_id, supplier_name);
