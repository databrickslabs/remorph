--Query type: DML
DECLARE @e1 INT = -20001, @e2 INT = -20002, @selector BIT = 1;
DECLARE @inner_e1 INT = -20003, @inner_e2 INT = -20004, @inner_selector BIT = 1;
DECLARE @error_message NVARCHAR(4000);

BEGIN
    IF (@selector = 1)
        THROW @e1, 'Exception @e1', 1;
    ELSE
        THROW @e2, 'Exception @e2', 1;
END;

BEGIN TRY
    IF (@inner_selector = 1)
        THROW @inner_e1, 'Inner Exception @inner_e1', 1;
    ELSE
        THROW @inner_e2, 'Inner Exception @inner_e2', 1;
END TRY
BEGIN CATCH
    SELECT @error_message = ERROR_MESSAGE();
    SELECT @error_message AS ErrorMessage;
END CATCH;