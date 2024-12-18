-- tsql sql:
CREATE TABLE #Vehicles
(
    Vehicle_Type VARCHAR(15),
    Vehicle_Price MONEY,
    Vehicle_Color VARCHAR(10)
);

INSERT #Vehicles
SELECT *
FROM (
    VALUES
    (
        'truck',
        12000,
        'green'
    ),
    (
        'bus',
        18000,
        'yellow'
    ),
    (
        'train',
        25000,
        'green'
    ),
    (
        'airplane',
        50000,
        'silver'
    )
) AS Vehicle_CTE(Vehicle_Type, Vehicle_Price, Vehicle_Color);
