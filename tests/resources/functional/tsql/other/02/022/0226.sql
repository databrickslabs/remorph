--Query type: DML
CREATE PROCEDURE my_anomaly_detector
    @INPUT_DATA sys.sql_variant,
    @TIMESTAMP_COLNAME nvarchar(128),
    @TARGET_COLNAME nvarchar(128)
AS
BEGIN
    WITH my_cte AS (
        SELECT
            c_custkey,
            c_name,
            c_address,
            c_phone,
            c_acctbal,
            c_mktsegment,
            c_comment,
            current_timestamp AS timestamp_column
        FROM
            #Customer
    )
    SELECT
        my_cte.c_acctbal AS target_column,
        my_cte.timestamp_column AS timestamp_column
    FROM
        my_cte;
END;
EXEC my_anomaly_detector
    @INPUT_DATA = NULL,
    @TIMESTAMP_COLNAME = 'timestamp_column',
    @TARGET_COLNAME = 'c_acctbal';
SELECT * FROM #Customer;
DROP TABLE #Customer;
