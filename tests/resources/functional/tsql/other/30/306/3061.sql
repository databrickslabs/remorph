-- tsql sql:
WITH CitiesCTE AS ( SELECT TOP 1 c_custkey, c_name, c_address FROM customer ) UPDATE c SET c.X = 23.5 FROM (VALUES (10.5, 'New York'), (20.8, 'Los Angeles'), (30.1, 'Chicago')) c (X, Name) INNER JOIN CitiesCTE ct ON c.Name = ct.c_name WHERE ct.c_name = 'New York';
