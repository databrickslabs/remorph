SELECT * 
    FROM (
         SELECT i, p, o, 
                ROW_NUMBER() OVER (PARTITION BY p ORDER BY o) AS row_num
            FROM qt
        )
    WHERE row_num = 1
    ;