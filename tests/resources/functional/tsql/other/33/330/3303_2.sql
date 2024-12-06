-- tsql sql:
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'employeeInfo')
BEGIN
    CREATE TABLE employeeInfo
    (
        emp_id INT,
        emp_code VARCHAR(50),
        salary DECIMAL(10, 2),
        emp_dept VARCHAR(50),
        emp_fname NVARCHAR(50),
        emp_lname NVARCHAR(50),
        emp_age INT
    );
END

-- Insert data into the table
INSERT INTO employeeInfo (emp_id, emp_code, salary, emp_dept, emp_fname, emp_lname, emp_age)
VALUES
    (102, 'USA-987-02', 25000, 'R-M53550M', N'Mendel', N'Roland', 32),
    (103, 'USA-987-03', 28000, 'R-M53550M', N'John', N'Doe', 35);

-- Select all data from the table
SELECT * FROM employeeInfo;

-- REMORPH CLEANUP: DROP TABLE employeeInfo;
