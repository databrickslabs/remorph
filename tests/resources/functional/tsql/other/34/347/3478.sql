--Query type: DML
CREATE TABLE #T (Instructions xml);
INSERT INTO #T (Instructions)
VALUES (
    '<root xmlns="https://schemas.microsoft.com/sqlserver/2004/07/adventure-works/ProductModelManuInstructions">
        <Location LocationID="1000" LaborHours="500" />
    </root>'
);
DECLARE @xmlns nvarchar(100) = 'https://schemas.microsoft.com/sqlserver/2004/07/adventure-works/ProductModelManuInstructions';

UPDATE #T
SET Instructions.modify('
    declare namespace MI="' + @xmlns + '";
    insert attribute LaborHours { "1000" } into (/MI:root/MI:Location[@LocationID=1000])[1]
');

SELECT Instructions
FROM #T;
-- REMORPH CLEANUP: DROP TABLE #T;
