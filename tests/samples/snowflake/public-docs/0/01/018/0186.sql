select w2
    from wildcards
    where regexp_like(w2, '\\' || '?');