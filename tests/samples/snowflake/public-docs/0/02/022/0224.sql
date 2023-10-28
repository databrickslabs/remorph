SELECT v,
       COLLATION(v),
       COLLATE(v, 'sp-upper'),
       COLLATION(COLLATE(v, 'sp-upper'))
    FROM collation1;