--Query type: DQL
DECLARE @s geometry = 'CURVEPOLYGON(COMPOUNDCURVE(CIRCULARSTRING(1 5, 5 1, 9 5), (9 5, 1 5)))';
SELECT @s.BufferWithCurves(2).ToString();
