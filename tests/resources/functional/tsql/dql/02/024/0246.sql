--Query type: DQL
CREATE PROCEDURE my_schema.my_stored_procedure_GET_DATA_LIMIT
AS
BEGIN
    WITH temp_result AS
    (
        SELECT *
        FROM
        (
            VALUES
            (1, 'test'),
            (2, 'test2')
        ) AS t (id, name)
    )
    SELECT *
    FROM temp_result;
END;

EXECUTE my_schema.my_stored_procedure_GET_DATA_LIMIT;

-- REMORPH CLEANUP: DROP PROCEDURE my_schema.my_stored_procedure_GET_DATA_LIMIT;
