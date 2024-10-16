--Query type: DQL
WITH xml_data AS (
    SELECT CAST('<Customer><FName>John</FName><LName>Doe</LName></Customer>' AS xml) AS customer_xml
)
SELECT customer_xml
FROM xml_data;