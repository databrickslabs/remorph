--Query type: DML
DECLARE @Hrs INT = 10;
DECLARE @myDoc XML = (
    SELECT *
    FROM (
        VALUES ('<Root><Location LocationID="10"/></Root>')
    ) AS T(XmlData)
);
SET @myDoc.modify('insert attribute MachineHours {sql:variable("@Hrs") } into   (/Root/Location[@LocationID=10])[1]');
SELECT @myDoc;
