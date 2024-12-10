-- tsql sql:
CREATE PROCEDURE Get_Current_DB
AS
BEGIN
	WITH temp AS (
		SELECT DB_NAME() AS CurrentDB
	)
	SELECT *
	FROM temp;
END;
