-- tsql sql:
DECLARE @myDoc xml;
SET @myDoc = (
    SELECT *
    FROM (
        SELECT 1 AS LocationID, 'Location1' AS LocationName
        UNION ALL
        SELECT 2, 'Location2'
        UNION ALL
        SELECT 3, 'Location3'
    ) AS LocationCTE
    FOR XML PATH('Location'), ROOT('Root')
);
SET @myDoc.modify('insert (
    attribute SetupHours {".5"},
    attribute SomeOtherAtt {".2"}
) into (/Root/Location[@LocationID=1])[1]');
SELECT @myDoc;
