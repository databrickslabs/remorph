--Query type: DDL
CREATE TABLE CustomerLocations
(
    customer_id INT IDENTITY(1, 1),
    location GEOGRAPHY,
    location_text AS location.STAsText()
);

WITH temp_result AS
(
    SELECT 1 AS customer_id, GEOGRAPHY::Point(10, 10, 4326) AS location
)
INSERT INTO CustomerLocations (customer_id, location)
SELECT customer_id, location
FROM temp_result;

SELECT *
FROM CustomerLocations;
-- REMORPH CLEANUP: DROP TABLE CustomerLocations;