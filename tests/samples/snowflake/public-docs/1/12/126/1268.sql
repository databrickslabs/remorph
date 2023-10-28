SELECT * 
    FROM ilike_ex 
    WHERE subject ILIKE '%j%h%^_do%' ESCAPE '^'
    ORDER BY 1;