--Query type: DQL
DECLARE @id INT, @indid INT;
SET @id = OBJECT_ID('customer');

WITH indexes AS (
    SELECT index_id, object_id, name
    FROM (
        VALUES (1, @id, 'index1'),
               (2, @id, 'index2')
    ) AS indexes (index_id, object_id, name)
)

SELECT @indid = index_id
FROM indexes
WHERE object_id = @id AND name = 'index1';
