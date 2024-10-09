--Query type: DML
IF OBJECT_ID('variant_example', 'U') IS NULL
CREATE TABLE variant_example (
    variant_column SQL_VARIANT
);
INSERT INTO variant_example (
    variant_column
)
SELECT variant_value
FROM (
    VALUES (13), (0)
) AS variant_values (
    variant_value
);
SELECT *
FROM variant_example;
-- REMORPH CLEANUP: DROP TABLE variant_example;