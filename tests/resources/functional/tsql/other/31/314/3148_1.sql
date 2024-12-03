--Query type: DML
CREATE TABLE new_employees (id_num INT IDENTITY(1,1), fname VARCHAR(40), minit CHAR(1), lname VARCHAR(40), email VARCHAR(50));
INSERT INTO new_employees (fname, minit, lname, email)
VALUES ('Karin', 'F', 'Josephs', 'karin.josephs@example.com'), ('Pirkko', 'O', 'Koskitalo', 'pirkko.koskitalo@example.com');
