-- tsql sql:
CREATE XML SCHEMA COLLECTION dbo.lineitem_xml AS ' <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"> <xs:element name="lineitem" type="xs:string"/> </xs:schema>' ;
WITH cte_lineitem AS (
    SELECT 'lineitem1' AS lineitem
)
SELECT *
FROM cte_lineitem
FOR XML PATH('lineitem'), ROOT('lineitems');
-- REMORPH CLEANUP: DROP XML SCHEMA COLLECTION dbo.lineitem_xml;
