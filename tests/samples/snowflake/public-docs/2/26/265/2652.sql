SELECT ID, array1, array2, tip, ARRAY_INTERSECTION(array1, array2) 
    FROM array_demo
    WHERE ID <= 3
    ORDER BY ID;