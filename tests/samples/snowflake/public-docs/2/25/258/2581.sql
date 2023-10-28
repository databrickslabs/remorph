SELECT OBJECT_CONSTRUCT(*) AS oc,
       OBJECT_CONSTRUCT_KEEP_NULL(*) AS oc_keep_null
    FROM demo_table_1
    ORDER BY oc_keep_null['PROVINCE'];