-- tsql sql:
DECLARE @g geography;
SET @g = (
    SELECT geo
    FROM (
        VALUES (
            geography::STPointFromWKB(0x010100000017D9CEF753D347407593180456965EC0, 4326)
        )
    ) AS temp(geo);
SELECT @g.ToString() AS GeographyString;
