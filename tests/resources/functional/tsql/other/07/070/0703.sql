--Query type: DML
CREATE TABLE target_table
(
    id INT PRIMARY KEY,
    description VARCHAR(100)
);

CREATE TABLE source_table
(
    id INT PRIMARY KEY,
    description VARCHAR(100)
);

INSERT INTO source_table (id, description)
VALUES
    (1, 'Description 1'),
    (2, 'Description 2'),
    (3, 'Description 3');

WITH source_data AS
(
    SELECT id, description
    FROM source_table
)
MERGE INTO target_table AS target
USING source_data AS source
ON target.id = source.id
WHEN MATCHED THEN
    UPDATE SET target.description = source.description
WHEN NOT MATCHED THEN
    INSERT (id, description)
    VALUES (source.id, source.description);

SELECT * FROM target_table;

-- REMORPH CLEANUP: DROP TABLE target_table;
-- REMORPH CLEANUP: DROP TABLE source_table;