-- tsql sql:
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'target_clone')
BEGIN
    EXEC('CREATE SCHEMA target_clone');
END;

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'target' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    CREATE TABLE dbo.target (
        id INT,
        name VARCHAR(50)
    );
END;

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'target' AND schema_id = SCHEMA_ID('target_clone'))
BEGIN
    CREATE TABLE target_clone.target (
        id INT,
        name VARCHAR(50)
    );
END;

INSERT INTO dbo.target (id, name)
VALUES
    (1, 'John'),
    (2, 'Alice');

WITH target_data AS
(
    SELECT id, name
    FROM dbo.target
)
INSERT INTO target_clone.target (id, name)
SELECT id, name
FROM target_data;

WITH target_clone_data AS
(
    SELECT id, name
    FROM target_clone.target
)
SELECT *
FROM target_clone_data;

SELECT *
FROM (
    SELECT id, name
    FROM target_clone.target
) AS target_clone_data_derived;

-- REMORPH CLEANUP: DROP TABLE target_clone.target;
-- REMORPH CLEANUP: DROP TABLE dbo.target;
-- REMORPH CLEANUP: DROP SCHEMA target_clone;
