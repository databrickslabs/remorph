--Query type: DDL
IF OBJECT_ID('[repair_table_temp_2]', 'U') IS NOT NULL
    DROP TABLE [repair_table_temp_2];

CREATE TABLE [repair_table_temp_2]
(
    id INT,
    name VARCHAR(255)
);

INSERT INTO [repair_table_temp_2] (id, name)
VALUES
    (1, 'John'),
    (2, 'Alice');

IF OBJECT_ID('[repair_table_temp_2]', 'U') IS NOT NULL
    DROP TABLE [repair_table_temp_2];
-- REMORPH CLEANUP: DROP TABLE [repair_table_temp_2];