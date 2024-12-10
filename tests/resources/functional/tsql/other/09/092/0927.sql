-- tsql sql:
CREATE DATABASE TestDB4 ( EDITION = 'GeneralPurpose' );
WITH TempResult AS (
    SELECT 'Database Created Successfully' AS Message
)
SELECT * FROM TempResult;
