SELECT SYSTEM$EXPLAIN_PLAN_JSON(
    $$ SELECT symptom, IFNULL(diagnosis, '(not yet diagnosed)') FROM medical $$
    );