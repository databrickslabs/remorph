-- tsql sql:
CREATE PROCEDURE generate_numbers
AS
BEGIN
    SELECT *
    FROM (
        VALUES (1), (2), (3), (4), (5)
    ) AS numbers(n);
END;
