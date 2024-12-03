--Query type: DQL
WITH temp_tables AS (
    SELECT 'Table1' AS name, 1 AS object_id
),
     temp_indexes AS (
    SELECT 'Index1' AS name, 1 AS object_id, 1 AS data_space_id, 'INDEX' AS type_desc
),
     temp_filegroups AS (
    SELECT 'Filegroup1' AS name, 1 AS data_space_id
)
SELECT tt.name AS [Table Name],
       ti.name AS [Index Name],
       ti.type_desc,
       ti.data_space_id,
       tf.name AS [Filegroup Name]
FROM temp_indexes AS ti
     JOIN temp_filegroups AS tf ON ti.data_space_id = tf.data_space_id
     JOIN temp_tables AS tt ON ti.object_id = tt.object_id
          AND ti.object_id = OBJECT_ID(N'TPC_H.Customer', 'U');
