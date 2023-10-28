SELECT
    column1,
    CASE
        WHEN column1=1 THEN 'one'
        WHEN column1=2 THEN 'two'
        ELSE 'other'
    END AS result
FROM (values(1),(2),(3)) v;