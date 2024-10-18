--Query type: DML
INSERT INTO demo_table (id, name)
SELECT id, name
FROM (
    VALUES (1, 'John Doe')
) AS temp_table(id, name);