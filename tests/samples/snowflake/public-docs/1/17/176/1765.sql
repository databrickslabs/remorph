SELECT v
    FROM strings
    WHERE v REGEXP 'San* [fF].*'
    ORDER BY v;