--Query type: DML
CREATE TABLE mynewtable
(
    date_column DATE,
    timestamp_column1 DATETIME2(3),
    timestamp_column2 DATETIME2(3)
);

WITH temp_table AS
(
    SELECT CONVERT(DATE, '2013-05-08T23:39:20.123') AS date_column,
           CONVERT(DATETIME2(3), '2013-05-08T23:39:20.123') AS timestamp_column1,
           CONVERT(DATETIME2(3), '2013-05-08T23:39:20.123') AS timestamp_column2
)
INSERT INTO mynewtable (date_column, timestamp_column1, timestamp_column2)
SELECT date_column, timestamp_column1, timestamp_column2
FROM temp_table;

SELECT * FROM mynewtable;
-- REMORPH CLEANUP: DROP TABLE mynewtable;