-- see https://docs.snowflake.com/en/sql-reference/functions/st_collect

CREATE TABLE geo3 (g1 GEOGRAPHY, g2 GEOGRAPHY);
INSERT INTO geo3 (g1, g2) VALUES
    ( 'POINT(-180 -90)', 'POINT(-45 -45)' ),
    ( 'POINT(   0   0)', 'POINT(-60 -60)' ),
    ( 'POINT(+180 +90)', 'POINT(+45 +45)' );