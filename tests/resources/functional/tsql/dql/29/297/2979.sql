--Query type: DQL
WITH series AS ( SELECT * FROM GENERATE_SERIES(1, 10) ) SELECT * FROM series;
