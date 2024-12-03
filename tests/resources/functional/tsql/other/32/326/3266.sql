--Query type: DDL
CREATE TABLE #inventory (part_id INT IDENTITY(100, 1) NOT NULL, description VARCHAR(30) NOT NULL, entry_person VARCHAR(30) NOT NULL DEFAULT USER);
SELECT * FROM (VALUES ('Product A', USER), ('Product B', USER)) AS inventory(description, entry_person);
