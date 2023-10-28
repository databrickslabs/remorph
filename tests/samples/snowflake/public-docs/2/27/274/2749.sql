SELECT ID, try_parse_json(v) 
    FROM vartab
    ORDER BY ID;