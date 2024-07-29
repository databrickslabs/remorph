
-- snowflake sql:

                    CREATE TABLE employee (employee_id INT,
                        first_name VARCHAR(50) NOT NULL,
                        last_name VARCHAR(50) NOT NULL,
                        birth_date DATE,
                        hire_date DATE,
                        salary DECIMAL(10, 2),
                        department_id INT)
                ;

-- databricks sql:

            create table employee (employee_id decimal(38, 0),
                first_name string not null,
                last_name string not null,
                birth_date date,
                hire_date date,
                salary decimal(10, 2),
                department_id decimal(38, 0))
        ;
