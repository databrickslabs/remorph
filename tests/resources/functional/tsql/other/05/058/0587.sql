-- tsql sql:
SELECT *
FROM (
    VALUES ('index_name', 'NONCLUSTERED', 0)
) AS IndexInfo (
    name,
    type_desc,
    is_disabled
);
