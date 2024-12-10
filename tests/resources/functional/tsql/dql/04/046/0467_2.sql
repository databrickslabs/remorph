-- tsql sql:
DECLARE my_indexes CURSOR FOR
    SELECT
        my_object_name,
        my_object_id,
        my_index_id,
        my_logical_frag
    FROM
    (
        VALUES
            ('object1', 1, 10, 5),
            ('object2', 2, 20, 10)
    ) AS my_fraglist (
        my_object_name,
        my_object_id,
        my_index_id,
        my_logical_frag
    )
    WHERE
        my_logical_frag >= 5
        AND INDEXPROPERTY (my_object_id, 'my_index_name', 'IndexDepth') > 0;
