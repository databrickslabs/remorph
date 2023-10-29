-- see https://docs.snowflake.com/en/sql-reference/functions/array_intersection

SELECT ID, array1, array2, tip, ARRAY_INTERSECTION(array1, array2) 
    FROM array_demo
    WHERE ID <= 3
    ORDER BY ID;