--Query type: DQL
DECLARE @customer geography = 'POINT(-122.358 47.653)';
SELECT @customer.BufferWithCurves(1).ToString() AS buffer;