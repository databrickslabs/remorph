-- tsql sql:
WITH myDoc AS (
    SELECT CAST('<Root> <Location LocationID="20" LaborHours="2.2" > <step>Manufacturing step 1 at this work center</step> <step>Manufacturing step 2 at this work center</step> </Location> </Root>' AS xml) AS myDoc
)
SELECT CAST(REPLACE(CAST(myDoc AS nvarchar(MAX)), '<Location LocationID="20" LaborHours="2.2" >', '<Location LocationID="20" LaborHours="2.2" MachineHours="1.5">') AS xml) AS ModifiedXML
FROM myDoc;
