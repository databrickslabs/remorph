-- see https://docs.snowflake.com/en/sql-reference/functions/as_timestamp

CREATE TABLE multiple_types (
    binary1 VARIANT,
    date1 VARIANT,
    decimal1 VARIANT,
    time1 VARIANT,
    timestamp1 VARIANT
    );
INSERT INTO multiple_types 
     (binary1, date1, decimal1, time1, timestamp1)
   SELECT 
     TO_VARIANT(TO_BINARY('F0A5')),
     TO_VARIANT(TO_DATE('2018-10-10')), 
     TO_VARIANT(TO_DECIMAL(1.23, 6, 3)),
     TO_VARIANT(TO_TIME('12:34:56')),
     TO_VARIANT(TO_TIMESTAMP_NTZ('2018-10-10 12:34:56'))
     ;