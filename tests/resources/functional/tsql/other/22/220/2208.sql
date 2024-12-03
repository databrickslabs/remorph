--Query type: DML
INSERT INTO likes (edge_id, from_id, to_id, rating)
SELECT EDGE_ID_FROM_PARTS(OBJECT_ID('likes'), dataset_key) AS edge_id,
       NODE_ID_FROM_PARTS(OBJECT_ID('Person'), ID) AS from_id,
       NODE_ID_FROM_PARTS(OBJECT_ID('Restaurant'), ID) AS to_id,
       rating
FROM (
    VALUES (1, 1, 5),
           (2, 2, 5)
) AS staging_data (ID, dataset_key, rating);
