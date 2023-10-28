SELECT v,
       v = 'ñ' AS "COMPARISON TO LOWER CASE",
       v = 'Ñ' AS "COMPARISON TO UPPER CASE",
       COLLATE(v, 'sp-upper'),
       COLLATE(v, 'sp-upper') = 'Ñ'
    FROM collation1;