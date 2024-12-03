--Query type: DDL
DECLARE @catalog_exists INT;
SET @catalog_exists = (SELECT COUNT(*) FROM sys.fulltext_catalogs WHERE name = 'customerCatalog');
IF @catalog_exists = 0
BEGIN
    CREATE FULLTEXT CATALOG customerCatalog;
END
CREATE TABLE #temp_result
(
    c_name VARCHAR(50),
    c_address VARCHAR(50),
    c_phone VARCHAR(20),
    c_phone_ext VARCHAR(10)
);
INSERT INTO #temp_result (c_name, c_address, c_phone, c_phone_ext)
VALUES ('John Doe', '123 Main St', '123-456-7890', '123');
CREATE FULLTEXT INDEX ON #temp_result
(
    c_name LANGUAGE 1033,
    c_address LANGUAGE 1033,
    c_phone LANGUAGE 1033,
    c_phone_ext LANGUAGE 1033
)
KEY INDEX PK_temp_result_c_name
ON customerCatalog
WITH STOPLIST = SYSTEM, CHANGE_TRACKING OFF, NO POPULATION;
SELECT * FROM #temp_result;
-- REMORPH CLEANUP: DROP TABLE #temp_result;
-- REMORPH CLEANUP: DROP FULLTEXT CATALOG customerCatalog;
