-- tsql sql:
CREATE TABLE ZY (Z_id INT IDENTITY(200, 10) PRIMARY KEY, Z_name VARCHAR(20) NULL);
INSERT ZY (Z_name)
SELECT name
FROM (VALUES ('cave'), ('mountain'), ('valley')) AS T(name);
SELECT * FROM ZY;
-- REMORPH CLEANUP: DROP TABLE ZY;
