--Query type: DDL
IF EXISTS (SELECT 1 FROM (VALUES ('IXML_LineItem_ExtendedPrice')) AS idx (name) WHERE name = 'IXML_LineItem_ExtendedPrice')
DROP INDEX IXML_LineItem_ExtendedPrice ON dbo.LineItem;