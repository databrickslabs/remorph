-- tsql sql:
DECLARE @customer geography = 'LINESTRING(-100 40, -100 -5, -80 -5)';
SELECT @customer.EnvelopeAngle();
