--Query type: DCL
SET DATEFORMAT ymd;
DECLARE @date_var datetime2 = '2011-05-12';
SET LANGUAGE english;
WITH temp_result AS (
    SELECT @date_var AS date_var
)
SELECT CONVERT(varchar(11), date_var, 120)
FROM temp_result;
