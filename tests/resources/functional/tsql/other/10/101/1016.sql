--Query type: DDL
SELECT *
FROM (
    VALUES (
        1,
        CAST('<xml>data</xml>' AS XML)
    )
) AS MyCTE (
    Id,
    XmlData
);
