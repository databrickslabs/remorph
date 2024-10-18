--Query type: DML
DECLARE @myDoc XML;
SET @myDoc = '<Root><Location MachineHours="1000" /></Root>';
SET @myDoc.modify('delete /Root/Location/@MachineHours');
WITH ModifiedXML AS (
    SELECT @myDoc AS XMLValue
)
SELECT XMLValue
FROM ModifiedXML;