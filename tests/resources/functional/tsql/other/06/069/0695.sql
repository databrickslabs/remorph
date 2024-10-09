--Query type: DML
CREATE TABLE varia (v nvarchar(max));
INSERT INTO varia (v)
SELECT CONCAT('{"key5": "', key5, '", "key6": "', key6, '"}') AS v
FROM OPENJSON('{"key5": "value5", "key6": "value6"}')
WITH (key5 nvarchar(50), key6 nvarchar(50));
SELECT * FROM varia;
-- REMORPH CLEANUP: DROP TABLE varia;