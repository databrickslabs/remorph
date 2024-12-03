--Query type: DQL
DECLARE @new_g geometry;
SET @new_g = geometry::STPointFromWKB(0x010100000000000000000059400000000000005940, 0);
WITH temp_result AS (
    SELECT @new_g AS geom
)
SELECT geom.STAsText()
FROM temp_result;
