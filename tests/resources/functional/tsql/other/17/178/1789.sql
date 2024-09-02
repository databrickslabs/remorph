--Query type: DML
DECLARE @g2 geography = 'CIRCULARSTRING(-71.093 42.358, -71.083 42.354, -71.083 42.363, -71.093 42.363, -71.093 42.358)';
SELECT geography_string
FROM (
    VALUES (@g2.ToString())
) AS temp_result(geography_string);
