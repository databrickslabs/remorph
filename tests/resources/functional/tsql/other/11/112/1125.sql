--Query type: DDL
CREATE TABLE DeliveryRoute (ADDRESS VARCHAR(50));

WITH DataToInsert AS (
  SELECT 'DELIVERY' AS ADDRESS
)

-- Insert data into the table
INSERT INTO DeliveryRoute (ADDRESS)
SELECT ADDRESS FROM DataToInsert;

-- Select data from the table
SELECT * FROM DeliveryRoute;

-- REMORPH CLEANUP: DROP TABLE DeliveryRoute;