--Query type: DCL
REVOKE INSERT ON schemas TO [customer];
CREATE TABLE schemas (
    schema_name sysname
);
INSERT INTO schemas (
    schema_name
)
SELECT schema_name
FROM (
    VALUES ('public')
) AS schemas (
    schema_name
);
SELECT *
FROM schemas;
-- REMORPH CLEANUP: DROP TABLE schemas;