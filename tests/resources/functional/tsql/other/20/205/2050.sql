--Query type: TCL
DECLARE @new_dialog_handle UNIQUEIDENTIFIER;
SELECT @new_dialog_handle = column1
FROM (
    VALUES ('your_actual_uniqueidentifier_value_here')
) AS temp_table (column1);

IF @new_dialog_handle IS NOT NULL
BEGIN
    PRINT 'Ending conversation with handle: ' + CONVERT(VARCHAR(50), @new_dialog_handle);
END

SELECT @new_dialog_handle AS DialogHandle;