-- tsql sql:
DECLARE @myDoc XML;
WITH XMLData AS (
    SELECT CONVERT(XML, '<Root><Location><step>Step 1</step><step>Step 2</step><step>Step 3</step></Location></Root>') AS xml_data
)
SELECT @myDoc = xml_data
FROM XMLData;
SET @myDoc.modify('delete /Root/Location/step[2]');
SELECT @myDoc;
