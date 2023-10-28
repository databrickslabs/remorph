SELECT w2
  FROM wildcards
  WHERE REGEXP_LIKE(w2, $$\?$$);