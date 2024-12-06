-- tsql sql:
SELECT * FROM (VALUES ('Tango', 1), ('Salsa', 2), ('Rumba', 3)) AS t2 (col2, col3) WHERE col2 = 'Tango' COLLATE Latin1_General_CI_AS;
