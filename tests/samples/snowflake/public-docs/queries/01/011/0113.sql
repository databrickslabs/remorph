-- see https://docs.snowflake.com/en/sql-reference/functions/to_geometry

ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';

SELECT TO_GEOMETRY('POINT(1820.12 890.56)');