--Query type: DQL
DECLARE @customer geography;
SET @customer = geography::Parse('CIRCULARSTRING(-71.088 42.315, -71.087 42.314, -71.087 42.316, -71.088 42.316, -71.088 42.315)');
WITH customer_cte AS (
    SELECT @customer AS geo
)
SELECT geo.STNumCurves() AS num_curves
FROM customer_cte