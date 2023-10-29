-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/merge-transact-sql?view=sql-server-ver16

MERGE INTO Sales.SalesReason AS tgt
USING (
    SELECT 'Recommendation', 'Other'
    UNION ALL    
    SELECT 'Review', 'Marketing'
    UNION ALL
    SELECT 'Internet', 'Promotion'
    ) AS src(NewName, NewReasonType)
    ON tgt.Name = src.NewName
WHEN MATCHED
    THEN
        UPDATE SET ReasonType = src.NewReasonType
WHEN NOT MATCHED BY TARGET
    THEN
        INSERT (Name, ReasonType)
        VALUES (NewName, NewReasonType);