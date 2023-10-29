-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/atan-transact-sql?view=sql-server-ver16

SELECT ATAN(45.87) AS atanCalc1,  
    ATAN(-181.01) AS atanCalc2,  
    ATAN(0) AS atanCalc3,  
    ATAN(0.1472738) AS atanCalc4,  
    ATAN(197.1099392) AS atanCalc5;