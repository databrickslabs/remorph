SELECT subject
    FROM like_ex
    WHERE subject NOT LIKE 'John%'
    ORDER BY subject;