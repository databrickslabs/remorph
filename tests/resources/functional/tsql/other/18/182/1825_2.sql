-- tsql sql:
DECLARE @myDoc XML = (SELECT doc FROM (VALUES ('<Root><Location>USA</Location></Root>') ) AS T(doc));
SET @myDoc.modify('delete /Root/Location/text()');
SELECT @myDoc;
