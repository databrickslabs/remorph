--Query type: DDL
CREATE PROCEDURE checkcustomer @param INT AS
BEGIN
    IF (SELECT c_acctbal FROM (VALUES (1, 100.0), (2, 200.0), (3, 300.0)) AS Customer(c_custkey, c_acctbal) WHERE c_custkey = @param) > 200.0
        RETURN 1
    ELSE
        RETURN 2;
END;
-- REMORPH CLEANUP: DROP PROCEDURE checkcustomer;