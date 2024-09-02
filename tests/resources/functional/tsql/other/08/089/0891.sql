--Query type: DML
INSERT INTO temp_result_set (first_name, last_name, phone_number, city, zip_code)
SELECT *
FROM (
    VALUES ('Astrid', 'Pena', '1-650-230-8467', 'San Francisco', 94116),
         ('Liam', 'Russell', '1-212-759-3751', 'New York', 10018)
) AS temp_result_set (first_name, last_name, phone_number, city, zip_code)