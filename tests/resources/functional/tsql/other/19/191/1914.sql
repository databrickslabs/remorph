-- tsql sql:
DECLARE @y XML;
SET @y = '<customer><name>John</name><age>30</age></customer>';

WITH customer_data AS (
    SELECT CAST(@y AS xml) AS xml_data
)

SELECT
    xml_data.value('(/customer/name)[1]', 'varchar(20)') AS customer_name,
    xml_data.value('(/customer/age)[1]', 'int') AS customer_age
FROM customer_data;
-- REMORPH CLEANUP: DROP TABLE customer_data;
