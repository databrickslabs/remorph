--Query type: DML
DECLARE @xml XML = '<Root> <Location LocationID="10" LaborHours=".1" MachineHours=".2" >Manu steps are described here. <step>Manufacturing step 1 at this work center</step> <step>Manufacturing step 2 at this work center</step> </Location> </Root>';
DECLARE @modifiedXml XML;
IF @xml.value('count(/Root/Location[1]/step)', 'int') > 3
BEGIN
    SET @modifiedXml = REPLACE(CONVERT(VARCHAR(MAX), @xml), 'LaborHours=".1"', 'LaborHours="3.0"');
END
ELSE
BEGIN
    SET @modifiedXml = REPLACE(CONVERT(VARCHAR(MAX), @xml), 'LaborHours=".1"', 'LaborHours="1.0"');
END
SELECT CONVERT(XML, @modifiedXml) AS modifiedDoc;
