--Query type: DDL
CREATE TABLE #customer_names
(
    first_name nvarchar(50),
    last_name nvarchar(50)
);

INSERT INTO #customer_names (first_name, last_name)
VALUES ('John', 'Doe'), ('Jane', 'Doe');

CREATE FULLTEXT INDEX ON #customer_names (first_name)
    KEY INDEX idx_customer_names
    WITH SEARCH PROPERTY LIST = spl_customer_names,
         CHANGE_TRACKING OFF,
         NO POPULATION;

SELECT *
FROM #customer_names;

-- REMORPH CLEANUP: DROP FULLTEXT INDEX ON idx_customer_names;
-- REMORPH CLEANUP: DROP TABLE #customer_names;
