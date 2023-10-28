SELECT id, id_1, employee_id
    FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
    WHERE id_1 = 101;