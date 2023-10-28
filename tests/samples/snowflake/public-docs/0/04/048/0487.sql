SELECT
      col_1,
      col_2,
      col_3,
      LEAST(col_1, col_2, col_3) AS least
    FROM (SELECT 1 AS col_1, 2 AS col_2, 3 AS col_3
          UNION ALL
          SELECT 2, 4, -1
          UNION ALL
          SELECT 3, 6, NULL
         );