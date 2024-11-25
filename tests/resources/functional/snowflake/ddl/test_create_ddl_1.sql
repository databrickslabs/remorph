-- snowflake sql:
CREATE TABLE employee (employee_id INT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  birth_date DATE,
  hire_date DATE,
  salary DECIMAL(10, 2),
  department_id INT,
  remarks VARIANT)
;

-- databricks sql:
CREATE TABLE employee (
  employee_id DECIMAL(38, 0),
  first_name STRING NOT NULL,
  last_name STRING NOT NULL,
  birth_date DATE,
  hire_date DATE,
  salary DECIMAL(10, 2),
  department_id DECIMAL(38, 0),
  remarks VARIANT
);
