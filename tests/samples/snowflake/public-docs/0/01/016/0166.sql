SELECT SUM(a) OVER (PARTITION BY x), SUM(b) OVER (PARTITION BY x) ... ;

SELECT SUM(a)                      , SUM(b) OVER (PARTITION BY x) ... ;