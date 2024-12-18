-- tsql sql:
CREATE TABLE Sales.District
WITH (DISTRIBUTION = REPLICATE)
AS
SELECT *
FROM (
    VALUES (1, 'North'),
           (2, 'South')
) AS District (District_id, District_Name);
