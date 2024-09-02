--Query type: DML
INSERT INTO returned_cars (car_ID)
SELECT car_ID
FROM (
    VALUES (201), (203), (205)
) AS temp (car_ID);