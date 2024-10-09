--Query type: DQL
SELECT LEAST('Acadia', 'Congaree', 'Crater Lake') AS LeastString
FROM (
    VALUES ('Acadia'),
           ('Congaree'),
           ('Crater Lake')
) AS NationalParks (ParkName);
