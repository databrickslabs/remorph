-- tsql sql:
DECLARE @g geography;
SET @g = (
    SELECT Geo
    FROM (
        VALUES (
            geography::STPolyFromWKB(0x01030000000100000005000000F4FDD478E9965EC0DD24068195D3474083C0CAA145965EC0508D976E12D3474083C0CAA145965EC04E62105839D44740F4FDD478E9965EC04E62105839D44740F4FDD478E9965EC0DD24068195D34740, 4326)
        )
    ) AS GeoTable(Geo)
);
SELECT @g.ToString();