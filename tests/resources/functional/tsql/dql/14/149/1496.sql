-- tsql sql:
DECLARE @GEO GEOGRAPHY = GEOGRAPHY::Parse('Polygon((-20 -20, -20 20, 20 20, 20 -20, -20 -20))');
WITH LocationCTE AS (
    SELECT @GEO.ReorientObject() AS ReorientedGeo
)
SELECT ReorientedGeo.STAsText() AS GeoText
FROM LocationCTE;
