-- see https://docs.snowflake.com/en/sql-reference/data-types-numeric

CREATE OR REPLACE TABLE test_fixed(num NUMBER,
                                    num10 NUMBER(10,1),
                                    dec DECIMAL(20,2),
                                    numeric NUMERIC(30,3),
                                    int INT,
                                    integer INTEGER
                                    );

DESC TABLE test_fixed;
