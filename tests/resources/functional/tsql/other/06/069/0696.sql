-- tsql sql:
CREATE TABLE xml_data (id INT, xml_col XML);
WITH temp_data AS (
    SELECT 1001 AS id, CONVERT(XML, '<customer> <name>John Doe</name> <address> <street>123 Main St</street> <city>Anytown</city> <state>CA</state> <zip>12345</zip> </address> </customer>') AS xml_col
)
INSERT INTO xml_data (id, xml_col)
SELECT id, xml_col
FROM temp_data;
SELECT * FROM xml_data;
-- REMORPH CLEANUP: DROP TABLE xml_data;
