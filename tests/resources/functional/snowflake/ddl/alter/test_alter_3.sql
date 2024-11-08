-- snowflake sql:
ALTER TABLE employee ADD COLUMN
age INT DEFAULT 30,
hire_date DATE NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- databricks sql:
ALTER TABLE employee   ADD COLUMNS
    age DECIMAL(38, 0) DEFAULT 30,
    hire_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP();