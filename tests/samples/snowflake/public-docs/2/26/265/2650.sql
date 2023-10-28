SELECT array_intersection(ARRAY_CONSTRUCT('A', 'B', 'B', 'B', 'C'), 
                          ARRAY_CONSTRUCT('B', 'B'));