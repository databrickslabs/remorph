-- tsql sql:
DECLARE @temp_result TABLE (product_key VARCHAR(10), product_name VARCHAR(50));
INSERT INTO @temp_result (product_key, product_name)
SELECT *
FROM (
    VALUES ('1', 'product1'),
           ('2', 'product2')
) AS t (product_key, product_name);
UPDATE @temp_result
SET product_key = 'new_key',
    product_name = 'new_name';
SELECT *
FROM @temp_result;
-- REMORPH CLEANUP: DROP TABLE @temp_result;
