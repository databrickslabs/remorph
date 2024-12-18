-- tsql sql:
WITH order_xml AS (
    SELECT CAST('<order OrderDate = "1995-01-01"/>' AS XML) AS order_xml
)
SELECT order_xml.exist('/order[(@OrderDate cast as xs:date?) eq xs:date("1995-01-01")]') AS found
FROM order_xml;
