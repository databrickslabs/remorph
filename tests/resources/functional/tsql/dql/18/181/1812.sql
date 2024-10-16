--Query type: DQL
DECLARE @product_id INT;
SET @product_id = 123;

WITH xml_data AS (
    SELECT CONVERT(XML, '<products><product id="' + CONVERT(VARCHAR(10), product_id) + '"><name>' + product_name + '</name></product></products>') AS xml_col
    FROM (
        VALUES (123, 'Product A'),
               (456, 'Product B')
    ) AS T (product_id, product_name)
)

SELECT xml_col
FROM xml_data
WHERE xml_col.exist('/products/product[@id=sql:variable("@product_id")]/name') = 1