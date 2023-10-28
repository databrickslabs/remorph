select w2, regexp_replace(w2, '(.old)', 'very \\1')
    from wildcards
    order by w2;