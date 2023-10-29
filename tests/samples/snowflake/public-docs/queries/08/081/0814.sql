-- see https://docs.snowflake.com/en/sql-reference/constructs/from

SELECT *
    FROM TABLE(Fibonacci_Sequence_UDTF(6.0::FLOAT));