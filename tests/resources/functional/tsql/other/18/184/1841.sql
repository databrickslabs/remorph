--Query type: DML
DECLARE @myvar2 VARCHAR(10);
SET @myvar2 = 'sdrawkcaB';
SELECT REVERSE(@myvar2) AS Reversed2
FROM (VALUES (1)) AS temp_table(temp_column);
-- REMORPH CLEANUP: DROP VARIABLE @myvar2;