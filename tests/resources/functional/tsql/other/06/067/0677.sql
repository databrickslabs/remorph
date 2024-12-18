-- tsql sql:
CREATE TABLE mynewtable (col1 DATE, col2 DATETIME);
INSERT INTO mynewtable (col1, col2)
SELECT CAST('2013-05-08' AS DATE), CAST('2013-05-08T23:39:20.123' AS DATETIME)
FROM (VALUES (1)) AS temp_result (dummy);
SELECT * FROM mynewtable;
