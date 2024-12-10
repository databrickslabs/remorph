-- tsql sql:
CREATE TABLE contractors (
  contractor_first VARCHAR(50),
  contractor_last VARCHAR(50),
  worknum VARCHAR(20),
  city VARCHAR(50),
  zip_code VARCHAR(10)
);

CREATE TABLE employees (
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  workphone VARCHAR(20),
  city VARCHAR(50),
  postal_code VARCHAR(10)
);

INSERT INTO contractors (contractor_first, contractor_last, worknum, city, zip_code)
VALUES
('John', 'Doe', '123-456-7890', 'New York', '10001'),
('Jane', 'Doe', '987-654-3210', 'Los Angeles', '90001');

WITH cte AS (
  SELECT contractor_first AS first_name, contractor_last AS last_name, worknum AS workphone, city, zip_code AS postal_code
  FROM contractors
)
INSERT INTO employees (first_name, last_name, workphone, city, postal_code)
SELECT first_name, last_name, workphone, city, postal_code
FROM cte;

SELECT * FROM employees;

-- REMORPH CLEANUP: DROP TABLE contractors;
-- REMORPH CLEANUP: DROP TABLE employees;
