--Query type: DML
WITH temp AS ( SELECT R_REGIONKEY FROM ( VALUES (1), (2), (3), (4), (5) ) AS temp(R_REGIONKEY) WHERE R_REGIONKEY = 1 ) DELETE r FROM #R_REGION r WHERE r.R_REGIONKEY IN ( SELECT R_REGIONKEY FROM temp ); SELECT * FROM #R_REGION;
