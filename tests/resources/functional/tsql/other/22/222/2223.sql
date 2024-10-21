--Query type: DML
MERGE INTO Customer_Reason AS tgt
USING (
    SELECT 1, 'Recommendation', 'Other'
    UNION ALL
    SELECT 2, 'Review', 'Marketing'
    UNION ALL
    SELECT 3, 'Internet', 'Promotion'
) AS src (C_Reason_SK, NewName, NewReasonType)
ON tgt.C_Reason_SK = src.C_Reason_SK
WHEN MATCHED THEN
    UPDATE SET C_Reason_ID = src.NewName, C_Reason_Desc = src.NewReasonType
WHEN NOT MATCHED BY TARGET THEN
    INSERT (C_Reason_SK, C_Reason_ID, C_Reason_Desc)
    VALUES (src.C_Reason_SK, src.NewName, src.NewReasonType);