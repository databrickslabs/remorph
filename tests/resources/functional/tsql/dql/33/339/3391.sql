--Query type: DQL
WITH temp_result AS (SELECT 'Cat_Desc' AS catalog_name, 'ItemCount' AS property_name)
SELECT fulltextcatalogproperty(catalog_name, property_name)
FROM temp_result;