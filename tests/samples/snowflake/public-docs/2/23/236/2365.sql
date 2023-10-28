SELECT i_col, COUNT(*), COUNT(j_col)
    FROM basic_example
    GROUP BY i_col
    ORDER BY i_col;