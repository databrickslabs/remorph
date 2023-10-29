-- see https://docs.snowflake.com/en/sql-reference/functions/st_azimuth

SELECT ST_AZIMUTH(
    TO_GEOMETRY('POINT(0 1)', TO_GEOMETRY('POINT(0 0)')
);
