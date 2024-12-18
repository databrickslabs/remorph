-- tsql sql:
DECLARE @images_stage VARCHAR(255) = 'path_to_images_stage';

IF NOT EXISTS (
    SELECT *
    FROM sys.tables
    WHERE name = 'images_table'
)
CREATE TABLE images_table (
    file_url VARCHAR(255),
    image_format VARCHAR(255),
    size INT,
    tags VARCHAR(MAX),
    dominant_color VARCHAR(255),
    relative_path VARCHAR(255)
);

WITH temp_result AS (
    SELECT
        file_url,
        image_format,
        size,
        tags,
        dominant_color,
        REPLACE(file_url_with_path, @images_stage, '') AS relative_path
    FROM (
        VALUES
            ('file_url_1', 'image_format_1', 100, 'tags_1', 'dominant_color_1', 'path_to_images_stage/file_url_1'),
            ('file_url_2', 'image_format_2', 200, 'tags_2', 'dominant_color_2', 'path_to_images_stage/file_url_2')
    ) AS data (
        file_url,
        image_format,
        size,
        tags,
        dominant_color,
        file_url_with_path
    )
)
SELECT *
INTO #images_table
FROM temp_result;

SELECT *
FROM #images_table;

-- REMORPH CLEANUP: DROP TABLE #images_table;
-- REMORPH CLEANUP: DROP TABLE images_table;
