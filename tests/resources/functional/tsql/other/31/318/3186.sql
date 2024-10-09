--Query type: DML
CREATE TABLE ErrorLog (ErrorID INT, ErrorTime DATETIME, ErrorMessage VARCHAR(255));
TRUNCATE TABLE ErrorLog;
INSERT INTO ErrorLog (ErrorID, ErrorTime, ErrorMessage)
VALUES (1, '2022-01-01 12:00:00', 'Error Message 1'),
       (2, '2022-01-02 13:00:00', 'Error Message 2');
SELECT *
FROM ErrorLog;
-- REMORPH CLEANUP: DROP TABLE ErrorLog;