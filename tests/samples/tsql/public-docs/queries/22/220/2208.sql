-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/edge-id-from-parts-transact-sql?view=sql-server-ver16

INSERT INTO likes($edge_id, $from_id, $to_id, rating)
SELECT EDGE_ID_FROM_PARTS(OBJECT_ID('likes'), dataset_key) as from_id
, NODE_ID_FROM_PARTS(OBJECT_ID('Person'), ID) as from_id
, NODE_ID_FROM_PARTS(OBJECT_ID('Restaurant'), ID) as to_id
, rating
FROM OPENROWSET (BULK 'person_likes_restaurant.csv',
    DATA_SOURCE = 'staging_data_source',
    FORMATFILE = 'format-files/likes.xml',
    FORMATFILE_DATA_SOURCE = 'format_files_source',
    FIRSTROW = 2) AS staging_data;
;