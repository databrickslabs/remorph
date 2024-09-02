--Query type: DDL
CREATE TABLE Region_Tracking (
    Region_id INT IDENTITY(1000, 1) NOT NULL,
    Nation_id INT NOT NULL,
    Last_update DATETIME NOT NULL DEFAULT GETDATE(),
    RRegion_tracking_user VARCHAR(30) NOT NULL DEFAULT SYSTEM_USER
);

WITH Region_Tracking_CTE AS (
    SELECT 1 AS Nation_id, GETDATE() AS Last_update, SYSTEM_USER AS RRegion_tracking_user
    FROM (
        VALUES (1), (2), (3)
    ) AS x(y)
)
INSERT INTO Region_Tracking (
    Nation_id,
    Last_update,
    RRegion_tracking_user
)
SELECT Nation_id, Last_update, RRegion_tracking_user
FROM Region_Tracking_CTE;

SELECT * FROM Region_Tracking;
-- REMORPH CLEANUP: DROP TABLE Region_Tracking;