-- snowflake sql:
CREATE TABLE employee (employee_id INT DEFAULT 3000,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL
  )
;

-- databricks sql:
CREATE TABLE employee (
  employee_id DECIMAL(38, 0) DEFAULT 3000,
  first_name STRING NOT NULL,
  last_name STRING NOT NULL
);
