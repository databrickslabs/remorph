-- tsql sql:
CREATE TABLE #DialogHandles
(
    new_dialog_handle1 UNIQUEIDENTIFIER,
    new_dialog_handle2 UNIQUEIDENTIFIER,
    new_dialog_handle3 UNIQUEIDENTIFIER,
    new_OrderMsg XML
);

WITH DialogHandles AS
(
    SELECT NEWID() AS new_dialog_handle1,
           NEWID() AS new_dialog_handle2,
           NEWID() AS new_dialog_handle3,
           '<NewOrderMsg>Construct message as appropriate for the application</NewOrderMsg>' AS new_OrderMsg
)
INSERT INTO #DialogHandles (new_dialog_handle1, new_dialog_handle2, new_dialog_handle3, new_OrderMsg)
SELECT new_dialog_handle1, new_dialog_handle2, new_dialog_handle3, new_OrderMsg
FROM DialogHandles;

SELECT *
FROM #DialogHandles;

-- REMORPH CLEANUP: DROP TABLE #DialogHandles;
