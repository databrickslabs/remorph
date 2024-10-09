--Query type: DQL
DECLARE @customer GEOGRAPHY = 'Point(1 1 1 1)';
WITH customer_cte AS (
    SELECT @customer AS geo
)
SELECT geo.Lat AS customer_latitude, geo.Long AS customer_longitude, geo.HasM AS customer_has_m, geo.HasZ AS customer_has_z
FROM customer_cte