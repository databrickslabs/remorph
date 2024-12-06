-- tsql sql:
DECLARE @new_g geometry = 'CURVEPOLYGON(COMPOUNDCURVE(CIRCULARSTRING(1 5, 5 1, 9 5), (9 5, 1 5)))';
SELECT @new_g.BufferWithCurves(3).ToString() AS buffer_result, *
FROM (
    VALUES (1, 1),
           (2, 2)
) AS cte(c_custkey, o_orderkey);
