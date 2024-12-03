--Query type: DML
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'binary_data')
CREATE TABLE binary_data (
    binary_value INT
);

INSERT INTO binary_data (binary_value)
SELECT value FROM (
    VALUES (85), (170)
) AS temp(value);

SELECT * FROM binary_data;

-- REMORPH CLEANUP: DROP TABLE binary_data;
