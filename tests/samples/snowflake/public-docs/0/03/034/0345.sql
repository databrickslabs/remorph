SELECT
    MONTHS_BETWEEN('2019-03-01'::DATE,
                   '2019-02-01'::DATE) AS MonthsBetween1,
    MONTHS_BETWEEN('2019-02-01'::DATE,
                   '2019-03-01'::DATE) AS MonthsBetween2
    ;