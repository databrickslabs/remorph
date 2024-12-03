--Query type: DDL
WITH new_view AS (
    SELECT
        x_tab_b.mycol AS x_mycol,
        x_tab_b.col5,
        x_tab_b.col6,
        y_tab_b.mycol AS y_mycol,
        y_tab_b.col7,
        y_tab_b.col8
    FROM
        (
            VALUES
                (1, 10, 'a'),
                (2, 20, 'b')
        ) AS x_tab_b (mycol, col5, col6)
    INNER JOIN
        (
            VALUES
                (1, 100, 'x'),
                (2, 200, 'y')
        ) AS y_tab_b (mycol, col7, col8)
    ON x_tab_b.mycol = y_tab_b.mycol
)
SELECT * FROM new_view;
