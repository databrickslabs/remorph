--Query type: DML
INSERT INTO new_bicycles (new_bicycle_ID, new_bicycle_name)
SELECT new_bicycle_ID, new_bicycle_name
FROM (
    VALUES (101, 'New Bicycle 1'),
           (102, 'New Bicycle 2')
) AS temp (new_bicycle_ID, new_bicycle_name);