--Query type: DML
CREATE TABLE #PartitionSettings
(
    PartitionNumber INT,
    XMLCompression BIT
);

INSERT INTO #PartitionSettings
(
    PartitionNumber,
    XMLCompression
)
VALUES
(
    1,
    0
),
(
    2,
    1
),
(
    3,
    0
),
(
    4,
    1
),
(
    5,
    0
),
(
    6,
    1
),
(
    7,
    1
),
(
    8,
    1
);

CREATE TABLE #TempTable
(
    id INT
);

WITH PartitionSettingsCTE AS
(
    SELECT PartitionNumber, XMLCompression
    FROM #PartitionSettings
)
SELECT 'ALTER TABLE #TempTable REBUILD PARTITION = ' + CONVERT(VARCHAR, PartitionNumber) + ' WITH (XML_COMPRESSION = ' + CONVERT(VARCHAR, XMLCompression) + ');' AS sql_statement
INTO #sql_statements
FROM PartitionSettingsCTE;

DECLARE @sql_statement NVARCHAR(MAX);

DECLARE cur CURSOR FOR SELECT sql_statement FROM #sql_statements;

OPEN cur;

FETCH NEXT FROM cur INTO @sql_statement;

WHILE @@FETCH_STATUS = 0
BEGIN
    EXEC sp_executesql @sql_statement;
    FETCH NEXT FROM cur INTO @sql_statement;
END

CLOSE cur;

DEALLOCATE cur;

SELECT * FROM #TempTable;