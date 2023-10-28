SELECT
    MONTHS_BETWEEN('2019-03-28'::DATE,
                   '2019-02-28'::DATE) AS MonthsBetween1,
    MONTHS_BETWEEN('2019-03-30'::DATE,
                   '2019-02-28'::DATE) AS MonthsBetween2,
    MONTHS_BETWEEN('2019-03-31'::DATE,
                   '2019-02-28'::DATE) AS MonthsBetween3
    ;