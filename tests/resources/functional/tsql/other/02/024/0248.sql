-- tsql sql:
CREATE PROCEDURE sp_UpdateNotificationPreference
AS
BEGIN
    SELECT *
    FROM (
        VALUES (1, 'SMS', 1)
    ) AS CustomerSettings (
        CustomerID,
        NotificationPreference,
        MuteNotification
    );
END;

EXEC sp_UpdateNotificationPreference;
-- REMORPH CLEANUP: DROP PROCEDURE sp_UpdateNotificationPreference;
