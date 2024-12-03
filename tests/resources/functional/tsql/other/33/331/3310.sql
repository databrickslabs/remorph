--Query type: DDL
CREATE PROCEDURE CreateCustomerTableAndTrigger
AS
BEGIN
    CREATE TABLE #customer
    (
        id INT,
        column1 INT,
        column2 INT,
        column3 INT,
        column4 INT,
        column5 INT
    );

    INSERT INTO #customer
    (
        id,
        column1,
        column2,
        column3,
        column4,
        column5
    )
    VALUES
    (
        1,
        1,
        1,
        1,
        1,
        1
    );

    EXEC ('CREATE TRIGGER uCustomer2
    ON #customer
    AFTER UPDATE
    AS
    BEGIN
        IF UPDATE (column3)
            AND UPDATE (column5)
        BEGIN
            PRINT ''Columns 3 and 5 updated'';
        END
    END;');

    UPDATE #customer
    SET column3 = 2,
        column5 = 2
    WHERE id = 1;

    SELECT *
    FROM #customer;
END;

EXEC CreateCustomerTableAndTrigger;
-- REMORPH CLEANUP: DROP PROCEDURE CreateCustomerTableAndTrigger;
