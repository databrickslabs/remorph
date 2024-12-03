--Query type: DQL
DECLARE @g geometry;
SET @g = geometry::STGeomFromWKB(0x010200000003000000000000000000594000000000000059400000000000003440000000000080664000000000008066400000000000806640, 0);
SELECT @g.STAsText() AS spatial_text
FROM (
    VALUES (1)
) AS temp(column_name);
