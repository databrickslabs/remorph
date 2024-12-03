--Query type: DDL
CREATE TABLE regiondf (default_value VARCHAR(50) DEFAULT 'unknown');
INSERT INTO regiondf (default_value)
VALUES ('unknown');
SELECT *
FROM regiondf;
-- REMORPH CLEANUP: DROP TABLE regiondf;
