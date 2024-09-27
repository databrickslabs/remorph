
-- snowflake sql:

                                SELECT OBJECT_KEYS(object1), OBJECT_KEYS(variant1)
                                FROM objects_1
                                ORDER BY id;
                              ;

-- databricks sql:
SELECT JSON_OBJECT_KEYS(object1), JSON_OBJECT_KEYS(variant1) FROM objects_1 ORDER BY id NULLS LAST;
