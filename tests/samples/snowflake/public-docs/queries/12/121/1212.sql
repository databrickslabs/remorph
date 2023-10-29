-- see https://docs.snowflake.com/en/sql-reference/functions/array_intersection

SELECT ID, array1, array2, tip, ARRAY_INTERSECTION(array1, array2) 
    FROM array_demo
    WHERE ID >= 5 and ID <= 7
    ORDER BY ID;