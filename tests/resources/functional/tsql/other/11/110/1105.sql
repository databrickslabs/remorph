--Query type: DDL
CREATE PROCEDURE order_processing_procedure
AS
BEGIN
    DECLARE @Message VARCHAR(255);

    WHILE EXISTS (
        SELECT 1
        FROM #OrderProcessingQueue
    )
    BEGIN
        SELECT TOP 1 @Message = Message
        FROM #OrderProcessingQueue;

        PRINT 'Processing message: ' + @Message;

        DELETE FROM #OrderProcessingQueue
        WHERE Message = @Message;
    END
END

CREATE TABLE #OrderProcessingQueue (
    MessageID INT IDENTITY(1,1),
    Message VARCHAR(255)
);

INSERT INTO #OrderProcessingQueue (Message)
VALUES ('Process Order 1'), ('Process Order 2'), ('Process Order 3');

EXEC order_processing_procedure;

SELECT *
FROM #OrderProcessingQueue;

-- REMORPH CLEANUP: DROP TABLE #OrderProcessingQueue;
-- REMORPH CLEANUP: DROP PROCEDURE order_processing_procedure;
