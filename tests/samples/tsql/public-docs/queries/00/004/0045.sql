-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/merge-transact-sql?view=sql-server-ver16

-- Create a temporary table variable to hold the output actions.
DECLARE @SummaryOfChanges TABLE (Change VARCHAR(20));

MERGE INTO Sales.SalesReason AS tgt
USING (
    VALUES ('Recommendation', 'Other'),
        ('Review', 'Marketing'),
        ('Internet', 'Promotion')
    ) AS src(NewName, NewReasonType)
    ON tgt.Name = src.NewName
WHEN MATCHED
    THEN
        UPDATE
        SET ReasonType = src.NewReasonType
WHEN NOT MATCHED BY TARGET
    THEN
        INSERT (Name, ReasonType)
        VALUES (NewName, NewReasonType)
OUTPUT $action
INTO @SummaryOfChanges;

-- Query the results of the table variable.
SELECT Change,
    COUNT(*) AS CountPerChange
FROM @SummaryOfChanges
GROUP BY Change;