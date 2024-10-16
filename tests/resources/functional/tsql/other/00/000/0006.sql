--Query type: DDL
CREATE TABLE region_info (
    region_name NVARCHAR(50),
    region_description TEXT
);

INSERT INTO region_info
SELECT *
FROM (
    VALUES (
        CAST('North America' AS NVARCHAR(50)),
        CAST('This is a region in North America' AS TEXT)
    ),
    (
        CAST('South America' AS NVARCHAR(50)),
        CAST('This is a region in South America' AS TEXT)
    )
) AS temp_result(region_name, region_description);

SELECT *
FROM region_info;
-- REMORPH CLEANUP: DROP TABLE region_info;