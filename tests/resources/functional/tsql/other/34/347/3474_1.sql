--Query type: DCL
DECLARE @myXML XML = '<root><person><name>John</name><age>30</age></person></root>';
SELECT *
FROM (
    VALUES (@myXML)
) AS T (myXML);
