--Query type: DML
INSERT INTO target_table (ID, description)
SELECT ID, description
FROM (
    VALUES (10, 'To be updated (this is the new value)'),
           (20, 'This is another value'),
           (30, 'And this is yet another value')
) AS temp_table (ID, description);